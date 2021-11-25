from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, cpf, birth_date, password=None):#,business=None):
        if not email:
            raise ValueError('É obrigatório possuir endereço de e-mail')
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            cpf = cpf,
            birth_date = birth_date,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, cpf=None, birth_date=None, password=None):
        user = self.create_user(
            email,
            password = password,
            first_name = first_name,
            last_name = last_name,
            cpf = cpf,
            birth_date = birth_date
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField('Endereço de e-mail', unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    business = models.ForeignKey('Business', null=True, blank=True, on_delete=models.SET_NULL)
    cpf = models.CharField(max_length=11, null=True)
    birth_date = models.DateField('Data de nascimento', null=True, blank=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Business(models.Model):
    cnpj_cpf = models.CharField(max_length=14, unique=True)
    name = models.CharField(max_length=50, unique=True)
    register_date = models.DateField(default=timezone.now)
    # owner = 
    class Meta:
        verbose_name_plural = 'businesses'

    def __str__(self) -> str:
        return self.name
