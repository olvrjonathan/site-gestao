from django.urls import path
from user import views

urlpatterns = [
    path('', views.redirect, name = 'cadastro_redirect'),
    path('cadastro/', views.cadastro, name = 'cadastro'),
    path('sucesso/', views.sucesso, name = 'sucesso'),
    path('all/', views.all, name = 'all'),
]