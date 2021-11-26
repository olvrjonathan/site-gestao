from django.urls import path
from user import views

urlpatterns = [
    path('', views.redirect, name = 'entrar_redirect'),
    path('entrar/', views.entrar, name = 'entrar'),
    path('sair/', views.sair, name = 'sair'),
    path('sucesso/', views.sucesso, name = 'sucesso'),
    path('all/', views.all, name = 'all'),
    path('index/', views.index, name = 'index'),
]