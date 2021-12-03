from django.urls import path
from user import views

urlpatterns = [
    path('', views.redirect, name = 'entrar_redirect'),
    path('inicio/', views.inicio, name = 'inicio'),
    path('sair/', views.sair, name = 'sair'),
    path('sucesso/', views.sucesso, name = 'sucesso'),
    path('all/', views.all, name = 'all'),
    path('agenda/', views.agenda, name = 'agenda'),
    path('ajustes/', views.ajustes, name = 'ajustes'),
    path('negocio/', views.negocio, name = 'negocio'),
    path('relatorios/', views.relatorios, name = 'relatorios'),
    path('servicos/', views.servicos, name = 'servicos'),
    path('convite/', views.convite, name = 'convite')
]