from django.db import models
#from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, cpf, birth_date, password=None):
        if not email:
            raise ValueError('É obrigatório possuir endereço de e-mail')
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name.capitalize(),
            last_name = last_name.capitalize(),
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
    business = models.ForeignKey('Business', null=True, blank=True,
                                on_delete=models.SET_NULL, related_name='associated_business')
    cpf = models.CharField(max_length=11, null=True, blank=False)
    birth_date = models.DateField('Data de nascimento', null=True, blank=False)
    phone_number = models.CharField(max_length=11, null=True, blank=False, unique=True,
                                    help_text='Insira apenas dígitos no formato (xx) 98765-4321.')
    is_client = models.BooleanField(default=False)
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

    def get_phone(self):
        n = self.phone_number
        return f'({n[:2]}) {n[2:7]}-{n[7:]}'
    
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
    register_date = models.DateField(auto_now_add=True)
    ceo = models.OneToOneField('CustomUser', on_delete=models.RESTRICT,
                                related_name='business_ceo', blank=True, unique=True)
    invitations = models.ManyToManyField('CustomUser', related_name='user_invitations',
                                        blank=True, limit_choices_to={'business': None})
    class Meta:
        verbose_name_plural = 'businesses'

    def __str__(self) -> str:
        return self.name


class Service(models.Model):
    business = models.ForeignKey('Business', on_delete=models.CASCADE)
    category = models.ForeignKey('ServiceCategory', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300, blank=True)
    duration = models.DurationField()
    price = models.DecimalField(max_digits=7, decimal_places=2)


class ServiceCategory(models.Model):
    category = models.CharField(max_length=40)
    class Meta:
        verbose_name_plural = 'service categories'


class Booking(models.Model):
    service = models.OneToOneField('Service', on_delete=models.RESTRICT)
    client = models.ForeignKey('CustomUser', on_delete=models.SET_NULL,
                                null=True, limit_choices_to={'is_client': True})
    date_time = models.DateField()
    paid_out = models.BooleanField(default=False)
    comment = models.CharField(max_length=300, null=True)


# class Inventory(models.Model):
#     business = OneToOneField('Business', on_delete=models.RESTRICT,
#                             related_name='inventory_owner')
#     date_update = models.DateField(auto_now=True)
#     product_quantity = models.IntegerField()