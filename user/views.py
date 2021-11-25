from django.http import HttpResponseRedirect
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# from datetime import date
# from random import randint

# |linebreaksbr

def redirect(request):
    url_redirecionamento = reverse('cadastro')
    return HttpResponseRedirect(url_redirecionamento)

#@login_required
def cadastro(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return HttpResponseRedirect(reverse('all'))
        else:
            print(form)
            return HttpResponseRedirect(reverse('all'))
    else:
        form = CustomUserCreationForm()
        return render(request, 'user/cadastro.html', {'form': form})

def sucesso(request):
    return render(request, 'user/sucesso.html')

def all(request):
    context = {'users': CustomUser.objects.all()}
    return render(request, 'user/all.html', context)

def index(request):
    return render(request, 'user/index.html')