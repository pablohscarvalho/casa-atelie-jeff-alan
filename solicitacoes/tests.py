from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import DatabaseError, IntegrityError, transaction
from django.test import Client, TestCase
from django.urls import reverse
from .forms import SolicitacaoForm
from .models import SolicitacaoEscolar
from .services import criar_solicitacao, assumir_solicitacao, alterar_situacao

DADOS = dict(escola='Escola Exemplo', nome_contato='Pessoa de Teste',
             email_contato='educador@example.org', atividade_desejada='Visita educativa',
             periodo_pretendido='Manhã em março', quantidade_participantes=25)


class SolicitacaoTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_user('operador', password='Exemplo-apenas-teste-9087', is_staff=True)
        self.admin.user_permissions.set(Permission.objects.filter(content_type__app_label='solicitacoes', codename__in=['view_solicitacaoescolar', 'change_solicitacaoescolar']))

    def test_formulario_rejeita_campos_obrigatorios_ausentes(self):
        for campo in DADOS:
            with self.subTest(campo=campo):
                dados = DADOS.copy(); dados.pop(campo)
                self.assertFalse(SolicitacaoForm(dados).is_valid())

    def test_rejeita_email_quantidade_zero_negativa_e_fracao(self):
        for campo,valor in [('email_contato','incorreto'), ('quantidade_participantes',0), ('quantidade_participantes',-1), ('quantidade_participantes','1.5')]:
            with self.subTest(campo=campo,valor=valor):
                self.assertFalse(SolicitacaoForm({**DADOS,campo:valor}).is_valid())

    def test_criacao_ignora_campos_privilegiados(self):
        pedido = criar_solicitacao({**DADOS,'situacao':'confirmada','responsavel':self.admin.pk})
        self.assertEqual(pedido.situacao,'pendente'); self.assertIsNone(pedido.responsavel)

    def test_envio_integrado_grava_e_exibe_recebimento(self):
        response=self.client.post(reverse('solicitar'),DADOS,follow=True)
        self.assertEqual(SolicitacaoEscolar.objects.count(),1)
        self.assertContains(response,'ainda não estão confirmadas')

    def test_dados_invalidos_nao_gravam_e_preservam_entrada(self):
        response=self.client.post(reverse('solicitar'),{**DADOS,'email_contato':'invalido'})
        self.assertEqual(SolicitacaoEscolar.objects.count(),0)
        self.assertContains(response,'Escola Exemplo'); self.assertContains(response,'Revise a solicitação')

    def test_falha_de_banco_nao_exibe_sucesso(self):
        with patch('solicitacoes.views.criar_solicitacao',side_effect=DatabaseError('segredo SQL interno')):
            response=self.client.post(reverse('solicitar'),DADOS)
        self.assertContains(response,'Não foi possível registrar')
        self.assertNotContains(response,'segredo SQL interno')
        self.assertNotContains(response,'Solicitação recebida')

    def test_url_de_resultado_sem_envio_nao_afirma_sucesso(self):
        self.assertRedirects(self.client.get(reverse('recebida')),reverse('solicitar'))

    def test_csrf_obrigatorio(self):
        self.assertEqual(Client(enforce_csrf_checks=True).post(reverse('solicitar'),DADOS).status_code,403)

    def test_get_nao_grava(self):
        self.client.get(reverse('solicitar'),DADOS)
        self.assertEqual(SolicitacaoEscolar.objects.count(),0)

    def test_entrada_xss_escapada_na_reexibicao(self):
        response=self.client.post(reverse('solicitar'),{**DADOS,'escola':'<script>alert(1)</script>','email_contato':'invalido'})
        self.assertNotContains(response,'<script>alert(1)</script>')
        self.assertContains(response,'&lt;script&gt;')

    def test_fluxo_de_transicoes(self):
        pedido=criar_solicitacao(DADOS)
        assumir_solicitacao(pedido.pk,self.admin)
        pedido.refresh_from_db(); self.assertEqual(pedido.situacao,'pendente')
        alterar_situacao(pedido.pk,'em_analise',self.admin)
        alterar_situacao(pedido.pk,'confirmada',self.admin)
        pedido.refresh_from_db(); self.assertEqual(pedido.situacao,'confirmada')
        with self.assertRaises(ValidationError): alterar_situacao(pedido.pk,'pendente',self.admin)

    def test_recusa_apos_analise(self):
        pedido=criar_solicitacao(DADOS); assumir_solicitacao(pedido.pk,self.admin)
        alterar_situacao(pedido.pk,'em_analise',self.admin)
        alterar_situacao(pedido.pk,'recusada',self.admin)
        pedido.refresh_from_db(); self.assertEqual(pedido.situacao,'recusada')

    def test_bloqueia_salto_e_analise_sem_responsavel(self):
        pedido=criar_solicitacao(DADOS)
        for situacao in ['confirmada','em_analise']:
            with self.assertRaises(ValidationError): alterar_situacao(pedido.pk,situacao,self.admin)
        pedido.refresh_from_db(); self.assertEqual(pedido.situacao,'pendente')

    def test_nao_permite_assumir_duas_vezes(self):
        pedido=criar_solicitacao(DADOS); assumir_solicitacao(pedido.pk,self.admin)
        with self.assertRaises(ValidationError): assumir_solicitacao(pedido.pk,self.admin)

    def test_sem_permissao_nao_altera(self):
        usuario=get_user_model().objects.create_user('sempermissao',is_staff=True)
        pedido=criar_solicitacao(DADOS)
        with self.assertRaises(PermissionDenied): assumir_solicitacao(pedido.pk,usuario)
        with self.assertRaises(PermissionDenied): alterar_situacao(pedido.pk,'em_analise',usuario)

    def test_visitante_nao_consulta_administracao(self):
        response=self.client.get(reverse('admin:solicitacoes_solicitacaoescolar_changelist'))
        self.assertEqual(response.status_code,302)
        self.assertIn('/admin/login/',response.url)

    def test_staff_sem_permissao_nao_consulta_pedidos(self):
        usuario=get_user_model().objects.create_user('limitado',is_staff=True)
        self.client.force_login(usuario)
        self.assertEqual(self.client.get(reverse('admin:solicitacoes_solicitacaoescolar_changelist')).status_code,403)

    def test_admin_autorizado_consulta_e_assume_por_acao(self):
        pedido=criar_solicitacao(DADOS); self.client.force_login(self.admin)
        url=reverse('admin:solicitacoes_solicitacaoescolar_changelist')
        self.assertContains(self.client.get(url),'Escola Exemplo')
        self.client.post(url,{'action':'assumir','_selected_action':[str(pedido.pk)]})
        pedido.refresh_from_db(); self.assertEqual(pedido.responsavel,self.admin)

    def test_banco_rejeita_quantidade_zero(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            SolicitacaoEscolar.objects.create(**{**DADOS,'quantidade_participantes':0})

    def test_senha_nao_armazenada_em_texto_simples(self):
        self.assertTrue(self.admin.password.startswith('pbkdf2_sha256$'))
        self.assertNotIn('Exemplo-apenas-teste-9087',self.admin.password)
