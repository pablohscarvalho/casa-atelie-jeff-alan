from django import forms
from .models import SolicitacaoEscolar


class SolicitacaoForm(forms.ModelForm):
    """Lista explícita impede atribuição pública de situação e responsável."""
    class Meta:
        model = SolicitacaoEscolar
        fields = ["escola", "nome_contato", "email_contato", "atividade_desejada", "periodo_pretendido", "quantidade_participantes"]
        help_texts = {"periodo_pretendido": "Informe uma preferência. A data será combinada após avaliação."}
