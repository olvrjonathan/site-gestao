from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Business
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ('name', 'cnpj_cpf',)

class CustomUserLoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        widgets = {
            'password': forms.TextInput(attrs={'type': 'password'})
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'business', 'first_name', 'last_name', 'cpf', 'birth_date')
        labels = {
            'business': 'Associação empresarial',
            'cpf': 'CPF',
            'last_name': 'Sobrenome'
        }
        widgets = {
            'birth_date': forms.TextInput(attrs={'type': 'date'})
        }
    
    def validate(self):
        date = self.cleaned_data['birth_date']
        cpf = self.cleaned_data['cpf']
        if date > (datetime.date.today() - datetime.timedelta(days = 5844)):
            self.add_error('birth_date', 'Data inválida - Usuário muito jovem.')
        if len(cpf) < 11:
            self.add_error('cpf', 'Insira um CPF válido.')
        else:
            return True
        return False
        

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'business', )
        labels = {'business': 'Associação empresarial'}


#from crispy_forms.helper import FormHelper

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'business', 'cpf', 'email', 'birth_date',]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_class = ''