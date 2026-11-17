import logging
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods
from .forms import SolicitacaoForm
from .services import criar_solicitacao

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
def solicitar(request):
    form = SolicitacaoForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        try:
            criar_solicitacao(request.POST)
        except DatabaseError:
            logger.error("Falha de persistência ao registrar solicitação.")
            form.add_error(None, "Não foi possível registrar o pedido. Seus dados foram mantidos. Tente novamente.")
        except ValidationError:
            form.add_error(None, "Revise os dados da solicitação.")
        else:
            messages.success(request, "Solicitação recebida. A atividade e a data dependem de avaliação.", extra_tags="pedido_recebido")
            return redirect("recebida")
    return render(request, "solicitacoes/formulario.html", {"form": form})


@require_GET
def recebida(request):
    avisos = list(messages.get_messages(request))
    if not any("pedido_recebido" in aviso.tags.split() for aviso in avisos):
        return redirect("solicitar")
    return render(request, "solicitacoes/recebida.html")
