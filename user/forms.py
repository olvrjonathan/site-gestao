from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser, Business, ServiceAdd
#from django.core.exceptions import ValidationError
#from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, login
import datetime

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ('name', 'cnpj_cpf',)
        labels = {
            'name': 'Nome do negócio',
            'cnpj_cpf': 'Seu CPF/CNPJ da empresa'
        }

    def validate(self):
        if len(self.cleaned_data['cnpj_cpf']) in (11,14) and self.cleaned_data['cnpj_cpf'].isdigit():
            return True
        else:
            self.add_error('cnpj_cpf', 'Insira um CNPJ/CPF válido.')
            return False

#---------------------------------------------------------------------------------------------

class CustomUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'Endereço de e-mail ou senha incorretos.'
        super().__init__(*args, **kwargs)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'business', 'first_name', 'last_name', 'cpf', 'birth_date')
        labels = {
            'business': 'Associação empresarial',
            'cpf': 'CPF',
            'last_name': 'Sobrenome',
            'birth_date': 'Data de nascimento'
        }
        widgets = {
            'birth_date': forms.TextInput(attrs={'type': 'date'})
        }
    
    def validate(self):
        valid = True
        date = self.cleaned_data['birth_date']
        cpf = self.cleaned_data['cpf']
        if date > (datetime.date.today() - datetime.timedelta(days = 5844)):
            self.add_error('birth_date', 'Data inválida - Usuário muito jovem.')
            valid = False
        if len(cpf) < 11 or not cpf.isdigit():
            self.add_error('cpf', 'Insira um CPF válido.')
            valid = False
        return valid
        

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'business', )
        labels = {'business': 'Associação empresarial'}

#---------------------------------------------------------------------------------------------

class ServiceForm(forms.ModelForm):
    class Meta:
        model = ServiceAdd
        fields = ('business', 'description','price', 'duration','image')
        labels = {
            'business': 'Serviço',
            'description': 'Descrição',
            'price': 'Preço (R$)',
            'duration': 'Duração (min)',
            'image': 'Adicione uma imagem para o serviço'
        }
