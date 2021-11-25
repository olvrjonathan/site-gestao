from django.contrib import admin
from .models import Business

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informação pessoal', {'fields': ('first_name', 'last_name', 'cpf', 'birth_date')}),
        #('Permissões', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'cpf', 'birth_date'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Business)
