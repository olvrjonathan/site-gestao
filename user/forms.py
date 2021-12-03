from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser, Business
#from django.core.exceptions import ValidationError
#from django.utils.translation import ugettext_lazy as _
import datetime

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ('name', 'cnpj_cpf', 'ceo')
        labels = {
            'name': 'Nome do negócio',
            'cnpj_cpf': 'Seu CPF/CNPJ da empresa'
        }
        widgets = {'ceo': forms.HiddenInput()}

    def validate(self):
        self.cleaned_data['name'] = self.cleaned_data['name'].title()
        if len(self.cleaned_data['cnpj_cpf']) in (11,14) and self.cleaned_data['cnpj_cpf'].isdigit():
            return True
        else:
            self.add_error('cnpj_cpf', 'Insira um CNPJ/CPF válido.')
            return False


class ColaboratorForm(forms.Form):
    email = forms.EmailField(label='E-mail do colaborador')

    def validate(self):
        email = self.cleaned_data['email']
        if email in map(lambda x: x.email, CustomUser.objects.filter(business__isnull = False)):
            self.add_error('email', 'Usuário já é colaborador de um negócio.')
            return False
        if not CustomUser.objects.filter(email=email):
            self.add_error('email', 'Não há usuário cadastrado com este e-mail.')
            return False
        return True

#---------------------------------------------------------------------------------------------

class CustomUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'Endereço de e-mail ou senha incorretos.'
        super().__init__(*args, **kwargs)

    def validate(self):
        if self.is_client:
            self.add_error('email', 'Crie uma conta para entrar como usuário do serviço Hostess.')
            return False
        else:
            return True


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'cpf', 'birth_date')
        labels = {
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