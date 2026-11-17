from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class SolicitacaoEscolar(models.Model):
    class Situacao(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        EM_ANALISE = "em_analise", "Em análise"
        CONFIRMADA = "confirmada", "Confirmada"
        RECUSADA = "recusada", "Recusada"

    escola = models.CharField(max_length=200)
    nome_contato = models.CharField("nome do responsável", max_length=150)
    email_contato = models.EmailField("e-mail de contato")
    atividade_desejada = models.CharField(max_length=300)
    periodo_pretendido = models.CharField("período pretendido", max_length=200)
    quantidade_participantes = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    situacao = models.CharField(max_length=20, choices=Situacao.choices, default=Situacao.PENDENTE)
    responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criada_em", "-pk"]
        constraints = [
            models.CheckConstraint(condition=models.Q(quantidade_participantes__gte=1), name="participantes_positivos"),
            models.CheckConstraint(condition=models.Q(situacao__in=["pendente", "em_analise", "confirmada", "recusada"]), name="situacao_valida"),
            models.CheckConstraint(condition=models.Q(situacao="pendente") | models.Q(responsavel__isnull=False), name="analise_exige_responsavel"),
        ]

    def __str__(self):
        return f"Pedido {self.pk} — {self.escola}"
