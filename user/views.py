from django.http import HttpResponseRedirect
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from datetime import date
# from random import randint
#from django.utils import timezone

# |linebreaksbr

def redirect(request):
    return HttpResponseRedirect(reverse('entrar'))

def entrar(request):
    context = dict()
    if request.method != 'POST':
        context['signup'] = CustomUserCreationForm()
        context['credentials'] = CustomUserLoginForm()
    elif request.method == 'POST':
        if request.POST.get('reg'):
            signup = CustomUserCreationForm(request.POST)
            if signup.is_valid():
                if signup.validate():
                    user = signup.save(commit=False) # Permite alterações antes de salvar
                    user.save()
                    return HttpResponseRedirect(reverse('sucesso'))
            context['signup'] = signup
            context['credentials'] = CustomUserLoginForm()

        elif request.POST.get('log'):
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            print('--------------- Usuário:', user.first_name)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('sucesso'))
            context['signup'] = CustomUserCreationForm()
            context['credentials'] = CustomUserLoginForm(request.POST)
    
    return render(request, 'user/entrar.html', context)

@login_required
def sair(request):
    logout(request)
    return HttpResponseRedirect(reverse('entrar'))

def sucesso(request):
    return render(request, 'user/sucesso.html')

def all(request):
    context = {'users': CustomUser.objects.all()}
    return render(request, 'user/all.html', context)

def index(request):
    #return render(request, 'user/index.html')
    return HttpResponseRedirect(reverse('sucesso'))

def log_in(request):
    if request.method == "POST":
        credentials = CustomUserLoginForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        print(user.first_name)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('sucesso'))
        else:
            return render(request, 'user/login.html', {'login': credentials})
    else:
        credentials = CustomUserLoginForm()
        return render(request, 'user/login.html', {'login': credentials})