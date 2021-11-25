from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# class User(models.Model):

#     
#     email = models.EmailField()

class CustomUser(AbstractUser):
    #username = None
    #email = models.EmailField('Endereço de e-mail', unique=True)
    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = []

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    business = models.ForeignKey('Business', null=True, blank=True, on_delete=models.SET_NULL)
    cpf = models.CharField(max_length=11, unique=True)
    birth_date = models.DateField('Data de nascimento', null=True, blank=False)

    def __str__(self):
        return self.email


class Business(models.Model):
    cnpj_cpf = models.CharField(max_length=14, unique=True)
    name = models.CharField(max_length=50, unique=True)
    register_date = models.DateField(default=timezone.now)
    # owner = 
    class Meta:
        verbose_name_plural = 'businesses'

    def __str__(self) -> str:
        return self.name
