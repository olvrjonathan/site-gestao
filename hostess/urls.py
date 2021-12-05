from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import handler404, handler500
from user.views import pain
from client import views

handler404 = views.error404
handler500 = views.error500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cliente/', include('client.urls')),
    path('', include('user.urls')),
    path('trabalho/', include('trabalho.urls')),
    re_path(r'(accounts/login).*', pain) # Django insiste em redirecionar aqui quando o usuário
                                               # não está logado e acessa conteúdo que requer isso
]
