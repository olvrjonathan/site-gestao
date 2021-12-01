from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ClientCreationForm, ClientLoginForm


def redirect(request):
    return HttpResponseRedirect(reverse('entrar'))

def entrar(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('agendamento'))
    if request.method != 'POST':
        signup = ClientCreationForm()
        credentials = ClientLoginForm()
    elif request.method == 'POST':
        print(request.POST)
        if request.POST.get('reg'):
            signup = ClientCreationForm(request.POST)
            if signup.is_valid():
                if signup.validate():
                    user = signup.save(commit=False) # Permite alterações antes de salvar
                    user.save()
                    return HttpResponseRedirect(reverse('sucesso'))
        elif request.POST.get('log'):
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('sucesso'))
            credentials = ClientLoginForm(request.POST)
    context = {'signup': signup, 'credentials': credentials}
    return render(request, 'client/entrar.html', context)

@login_required
def sair(request):
    logout(request)
    return HttpResponseRedirect(reverse('entrar'))

def agendamento(request):
    return render(request, 'client/agendamento.html')
