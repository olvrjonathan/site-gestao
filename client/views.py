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
        if request.user.is_client:
            return HttpResponseRedirect(reverse('agendamento'))
        return HttpResponseRedirect(reverse('inicio'))
    signup = ClientCreationForm()
    credentials = ClientLoginForm()
    if request.method == 'POST':
        if request.POST.get('reg'):
            signup = ClientCreationForm(request.POST)
            if signup.is_valid():
                if signup.validate():
                    signup.save(commit=False)
                    signup.instance.is_client = True
                    signup.save()
                    return HttpResponseRedirect(reverse('entrar'))
        elif request.POST.get('log'):
            credentials = ClientLoginForm(request, data=request.POST)
            if credentials.is_valid():
                if credentials.validate():
                    email = credentials.cleaned_data.get('username')
                    password = credentials.cleaned_data.get('password')
                    user = authenticate(request, email=email, password=password)
                    if user:
                        if user.is_active:
                            login(request, user)
                            return HttpResponseRedirect(reverse('agendamento'))
            credentials = ClientLoginForm(request.POST)
    context = {'signup': signup, 'credentials': credentials}
    return render(request, 'client/entrar.html', context)

@login_required
def sair(request):
    logout(request)
    return HttpResponseRedirect(reverse('entrar'))

def agendamento(request):
    return render(request, 'client/agendamento.html')

def error404(request, exception):
    return render(request, '404.html', status=404)

def error500(request):
    return render(request, '500.html', status=500)
