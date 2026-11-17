from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from .models import SolicitacaoEscolar
from .services import assumir_solicitacao, alterar_situacao


@admin.register(SolicitacaoEscolar)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ["id", "escola", "situacao", "responsavel", "criada_em"]
    list_filter = ["situacao"]
    readonly_fields = [field.name for field in SolicitacaoEscolar._meta.fields]
    actions = ["assumir", "analisar", "confirmar", "recusar"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def executar(self, request, queryset, destino=None):
        total = 0
        for pedido_id in queryset.values_list("pk", flat=True):
            try:
                if destino is None:
                    assumir_solicitacao(pedido_id, request.user)
                else:
                    alterar_situacao(pedido_id, destino, request.user)
            except ValidationError as error:
                self.message_user(request, f"Pedido {pedido_id}: {'; '.join(error.messages)}", messages.ERROR)
            else:
                total += 1
        if total:
            self.message_user(request, f"{total} pedido(s) atualizado(s).", messages.SUCCESS)

    @admin.action(description="Assumir acompanhamento", permissions=["change"])
    def assumir(self, request, queryset):
        self.executar(request, queryset)

    @admin.action(description="Iniciar análise", permissions=["change"])
    def analisar(self, request, queryset):
        self.executar(request, queryset, "em_analise")

    @admin.action(description="Confirmar após avaliar disponibilidade e contatar escola", permissions=["change"])
    def confirmar(self, request, queryset):
        self.executar(request, queryset, "confirmada")

    @admin.action(description="Recusar solicitação", permissions=["change"])
    def recusar(self, request, queryset):
        self.executar(request, queryset, "recusada")
