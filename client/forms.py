from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
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
            self.add_error('phone_number', 'Insira um número de telefone válido (apenas dígitos).')
            return False
        return True


class ClientLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'Endereço de e-mail ou senha incorretos.'
        super().__init__(*args, **kwargs)

    def validate(self):
        if CustomUser.objects.get(email = self.cleaned_data['username']).is_client:
            return True
        else:
            self.add_error('username', 'Crie outra conta para acessar como cliente.')
            return False

class ClientChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', )
        labels = {'phone_number': 'Número de telefone'}