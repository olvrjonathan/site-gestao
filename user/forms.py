from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Business

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ('name', 'cnpj_cpf',)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'business', 'first_name', 'last_name', 'cpf', 'birth_date')
        labels = {
            'business': 'Associação empresarial',
            'cpf': 'CPF',
            'last_name': 'Sobrenome'
        }
        widgets = {
            'birth_date': forms.TextInput(attrs={'type': 'date'})
        }

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