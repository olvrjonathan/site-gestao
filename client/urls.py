from django.urls import path
from client import views

urlpatterns = [
    path('', views.redirect, name = 'entrar_redirect'),
    path('entrar/', views.entrar, name = 'entrar'),
    path('sair/', views.sair, name = 'sair'),
    path('agendamento/', views.agendamento, name = 'agendamento'),
]