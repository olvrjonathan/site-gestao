from django.http import HttpResponseRedirect, request
from .models import CustomUser, Business
from .forms import *
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
    return HttpResponseRedirect(reverse('inicio'))

@login_required
def sair(request):
    logout(request)
    return HttpResponseRedirect(reverse('inicio'))

def sucesso(request):
    return render(request, 'user/sucesso.html')

def all(request):
    context = {'users': CustomUser.objects.all()}
    return render(request, 'user/all.html', context)

def inicio(request):
    signup = CustomUserCreationForm()
    credentials = CustomUserLoginForm()
    modal = None
    if request.method == 'POST':
        if request.POST.get('reg'):
            signup = CustomUserCreationForm(request.POST)
            if signup.is_valid():
                if signup.validate():
                    signup.save()
                    return HttpResponseRedirect(reverse('inicio'))
            modal = 'registrar'
        elif request.POST.get('log'):
            credentials = CustomUserLoginForm(request, data=request.POST)
            if credentials.is_valid():
                email = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, email=email, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect(reverse('negocio'))
            modal = 'entrar'
    context = {'signup': signup, 'credentials': credentials, 'modal': modal}
    return render(request, 'user/inicio.html', context)

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
def negocio(request):
    is_owner = bool(Business.objects.filter(ceo=request.user.pk))
    is_worker = bool(request.user.business)
    if is_owner:
        condition = 'owner'
    elif is_worker:
        condition = 'worker'
    else:
        condition = 'free'
    modal = None
    business = None
    invites = None
    if not is_worker:
        business = BusinessForm()
        if request.method == 'POST':
            if request.POST.get('bus'):
                business = BusinessForm(request.POST)
                if business.is_valid():
                    if business.validate():
                        business.save(commit=False)
                        business.instance.ceo = request.user
                        pk = business.save().pk
                        user = CustomUser.objects.get(pk=request.user.pk)
                        user.business_id = pk
                        user.save()
                        business = BusinessForm()
                        return HttpResponseRedirect(reverse('negocio'))
                modal = 'business'
            if request.POST.get('accept') or request.POST.get('decline'):
                return convite(request)
        invites =  CustomUser.objects.get(pk=request.user.pk).user_invitations.all()
    elif condition == 'owner':
        to_add = Business.objects.get(pk=request.user.business.pk)
        business = ColaboratorForm()
        if request.method == 'POST':
            if request.POST.get('add'):
                business = ColaboratorForm(request.POST)
                if business.is_valid():
                    if business.validate():
                        user = CustomUser.objects.get(email=business.cleaned_data['email'])
                        to_add.invitations.add(user)
                        to_add.save()
                        business = ColaboratorForm()
                modal = 'add'
            if request.POST.get('erase') or request.POST.get('delete'):
                return convite(request)
        invites = to_add.invitations.all()
    elif condition == 'worker':
        if request.method == 'POST':
            if request.POST.get('leave'):
                return convite(request)
    context = {'condition': condition, 'business': business, 'modal': modal, 'invites': invites}
    return render(request, 'user/negocio.html', context)

@login_required
def relatorios(request):
    return render(request, 'user/relatorios.html')

@login_required
def servicos(request):
    return render(request, 'user/servicos.html')

@login_required
def convite(request):
    id = request.POST.get('id')
    if request.POST.get('decline'):
        request.user.user_invitations.remove(id)
    elif request.POST.get('accept'):
        request.user.business_id=id
        request.user.save()
        request.user.user_invitations.clear()
    elif request.POST.get('erase'):
        request.user.business.invitations.remove(id)
    elif request.POST.get('leave'):
        request.user.business_id = None
        request.user.save()
    elif request.POST.get('delete'):
        request.user.business.invitations.clear()
        request.user.business.delete()
        #Business.objects.filter(pk=id).delete()
    return HttpResponseRedirect(reverse('negocio'))