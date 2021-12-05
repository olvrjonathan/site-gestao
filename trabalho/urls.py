from django.urls import path
from trabalho import views

urlpatterns = [
    path('', views.inicio, name = 'inicio_trabalho'),
    path('marcelo/', views.marcelo, name = 'marcelo'),
    path('dominique/', views.dominique, name = 'dominique'),
    path('juliana/', views.juliana, name = 'juliana'),
    path('jonathan/', views.jonathan, name = 'jonathan'),
    path('iara/', views.iara, name = 'iara'),
]