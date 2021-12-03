from django.http import HttpResponseRedirect
from .models import CustomUser, Service
from .forms import BusinessForm, CustomUserChangeForm, CustomUserCreationForm, CustomUserLoginForm, BusinessForm, ServiceForm
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#from django.template import RequestContext
# from datetime import date
# from random import randint
#from django.utils import timezone

# |linebreaksbr

def redirect(request):
    return HttpResponseRedirect(reverse('index'))

@login_required
def sair(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def sucesso(request):
    return render(request, 'user/sucesso.html')

def all(request):
    context = {'users': CustomUser.objects.all()}
    return render(request, 'user/all.html', context)

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('sucesso'))
    signup = CustomUserCreationForm()
    credentials = CustomUserLoginForm()
    if request.method == 'POST':
        service_form = ServiceForm(data=request.POST, files=request.POST)
        if service_form.is_valid():
            service_form.save()
            obj = service_form.instance
            return render(request, "servicos.html",{"obj":obj})
        if request.POST.get('reg'):
            signup = CustomUserCreationForm(request.POST)
            if signup.is_valid():
                if signup.validate():
                    signup.save()
                    return HttpResponseRedirect(reverse('all'))
        elif request.POST.get('log'):
            credentials = CustomUserLoginForm(request, data=request.POST)
            if credentials.is_valid():
                email = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, email=email, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect(reverse('sucesso'))
    else:
        service_form = ServiceForm()
        img = Service.objects.all()
    context = {'signup': signup, 'credentials': credentials, 'img':img, 'service_form':service_form}
    return render(request, 'user/index.html', context)

@login_required
def negocio(request):
    return render(request, 'user/negocio.html')

@login_required
def agenda(request):
    return render(request, 'user/agenda.html')

@login_required
def ajustes(request):
    return render(request, 'user/ajustes.html')

@login_required
def estoque(request):
    return render(request, 'user/estoque.html')

@login_required
def negocio(request):
    return render(request, 'user/negocio.html')

@login_required
def relatorios(request):
    return render(request, 'user/relatorios.html')

@login_required
def servicos(request):
    return render(request, 'user/servicos.html')