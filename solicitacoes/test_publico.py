from unittest.mock import patch

from django.db import OperationalError
from django.test import TestCase
from django.urls import reverse


class PaginaPublicaTests(TestCase):
    def test_inicio_apresenta_o_espaco_e_oferece_solicitacao(self):
        response = self.client.get(reverse("inicio"))
        self.assertContains(response, "Casa Ateliê Jeff Alan")
        self.assertContains(response, 'href="/solicitar/"')
        self.assertContains(response, 'alt="Fachada iluminada da Casa Ateliê Jeff Alan')

    def test_saude_consulta_o_banco(self):
        response = self.client.get(reverse("saude"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
        self.assertEqual(response.headers["Cache-Control"], "no-store")

    def test_saude_responde_503_sem_detalhes_do_banco(self):
        with patch("solicitacoes.views.connection.cursor",
                   side_effect=OperationalError("detalhe interno")):
            response = self.client.get(reverse("saude"))
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"status": "unavailable"})
        self.assertEqual(response.headers["Cache-Control"], "no-store")
