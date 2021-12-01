from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from user.models import CustomUser
#from django.core.exceptions import ValidationError
#from django.utils.translation import ugettext_lazy as _


class ClientCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone_number')
        labels = {
            'first_name': 'Primeiro nome',
            'last_name': 'Sobrenome',
            'phone_number': 'Número de telefone'
        }
        widgets = {
            'phone_number': forms.TextInput(attrs={'type': 'tel'}) # tel, number
        }
    
    def validate(self):
        n = self.cleaned_data.get('phone_number')
        if not n.isdigit():
            self.add_error('phone_number', 'Insira um número de telefone válido.')
            return False
        return True


class ClientLoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        widgets = {
            'password': forms.TextInput(attrs={'type': 'password'})
        }

    def validate(self):
        if self.is_client:
            return True
        else:
            return False

class ClientChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', )
        labels = {'phone_number': 'Número de telefone'}