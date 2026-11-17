from django.contrib import admin
from django.urls import path
from solicitacoes import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("health/", views.saude, name="saude"),
    path("admin/", admin.site.urls),
    path("solicitar/", views.solicitar, name="solicitar"),
    path("solicitar/recebida/", views.recebida, name="recebida"),
]
