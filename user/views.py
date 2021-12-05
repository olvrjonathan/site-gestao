from django.http import HttpResponseRedirect
from .models import CustomUser, Business
from .forms import *
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# |linebreaksbr

def redirect(request):
    return HttpResponseRedirect(reverse('inicio'))

@login_required
def sair(request):
    logout(request)
    return HttpResponseRedirect(reverse('inicio'))

def inicio(request):
    if request.user.is_authenticated and request.user.is_client:
        return HttpResponseRedirect(reverse('entrar'))
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
def agenda(request):
    days = ['Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo']*2
    today = datetime.date.today().weekday()
    days = days[today-1:today+6]
    days[1] = 'Hoje'
    #pk = request.user.business.pk
    context = {'days': days, 'today': today, }
    return render(request, 'user/agenda.html', context)

@login_required
def ajustes(request):
    user = request.user
    data = {
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    form = CustomUserChangeForm(initial=data)
    modal = False
    if request.method == 'POST':
        if request.POST.get('delete_user'):
            return button(request)
        else:
            form = CustomUserChangeForm(request.POST, instance=user, initial=data)
            if form.has_changed():
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse('ajustes'))
                else:
                    modal = True
    context = {'form': form, 'modal': modal}
    return render(request, 'user/ajustes.html', context)

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
    colab = None
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
                return button(request)
        invites =  CustomUser.objects.get(pk=request.user.pk).user_invitations.all()
    elif condition == 'owner':
        colab = CustomUser.objects.filter(business=request.user.business.pk)
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
                return button(request)
        invites = to_add.invitations.all()
    elif condition == 'worker':
        colab = CustomUser.objects.filter(business=request.user.business.pk)
        if request.method == 'POST':
            if request.POST.get('leave'):
                return button(request)
    context = {'condition': condition, 'business': business, 'modal': modal, 'invites': invites, 'colab': colab}
    return render(request, 'user/negocio.html', context)

@login_required
def relatorios(request):
    return render(request, 'user/relatorios.html')

@login_required
def servicos(request):
    return render(request, 'user/servicos.html')

@login_required
def button(request):
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
    elif request.POST.get('delete_user'):
        user = request.user
        logout(request)
        user.delete()
    return HttpResponseRedirect(reverse('negocio'))

def pain(request, *args):
    return HttpResponseRedirect(reverse('inicio'))
