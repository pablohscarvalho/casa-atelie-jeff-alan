from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from .forms import SolicitacaoForm
from .models import SolicitacaoEscolar


def criar_solicitacao(dados):
    form = SolicitacaoForm(dados)
    if not form.is_valid():
        raise ValidationError(form.errors.as_json())
    with transaction.atomic():
        pedido = form.save(commit=False)
        pedido.situacao = SolicitacaoEscolar.Situacao.PENDENTE
        pedido.responsavel = None
        pedido.full_clean()
        pedido.save()
        return pedido


def verificar_permissao(usuario):
    if not (usuario.is_authenticated and usuario.is_active and usuario.is_staff
            and usuario.has_perm("solicitacoes.change_solicitacaoescolar")):
        raise PermissionDenied


@transaction.atomic
def assumir_solicitacao(pedido_id, usuario):
    verificar_permissao(usuario)
    pedido = SolicitacaoEscolar.objects.select_for_update().get(pk=pedido_id)
    if pedido.responsavel_id is not None:
        raise ValidationError("Este pedido já possui responsável.")
    pedido.responsavel = usuario
    pedido.full_clean()
    pedido.save(update_fields=["responsavel", "atualizada_em"])
    return pedido


@transaction.atomic
def alterar_situacao(pedido_id, nova_situacao, usuario):
    verificar_permissao(usuario)
    pedido = SolicitacaoEscolar.objects.select_for_update().get(pk=pedido_id)
    permitidas = {"pendente": {"em_analise"}, "em_analise": {"confirmada", "recusada"}}
    if nova_situacao not in permitidas.get(pedido.situacao, set()):
        raise ValidationError("Transição de situação não permitida.")
    if pedido.responsavel_id is None:
        raise ValidationError("Atribua um responsável antes de iniciar a análise.")
    pedido.situacao = nova_situacao
    pedido.full_clean()
    pedido.save(update_fields=["situacao", "atualizada_em"])
    return pedido
