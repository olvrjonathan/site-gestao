from django.urls import path
from trabalho import views

urlpatterns = [
    path('', views.inicio, name = 'inicio_trabalho'),
    path('marcelo/', views.marcelo, name = 'marcelo'),
]