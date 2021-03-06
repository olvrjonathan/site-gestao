# Generated by Django 3.2.5 on 2021-12-03 01:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnpj_cpf', models.CharField(max_length=14, unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('register_date', models.DateField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'businesses',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Endereço de e-mail')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('cpf', models.CharField(max_length=11, null=True)),
                ('birth_date', models.DateField(null=True, verbose_name='Data de nascimento')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('business', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.business')),
                ('is_client', models.BooleanField(default=False)),
                ('phone_number', models.CharField(help_text='Insira número no formato (xx) 98765-4321', max_length=11, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name_plural': 'service categories',
            },
        ),
        migrations.AddField(
            model_name='business',
            name='ceo',
            field=models.OneToOneField(default=2, on_delete=django.db.models.deletion.RESTRICT, related_name='business_ceo', to='user.customuser'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='business',
            name='register_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='business',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='associated_business', to='user.business'),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=300)),
                ('duration', models.DurationField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.business')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.servicecategory')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateField()),
                ('paid_out', models.BooleanField(default=False)),
                ('comment', models.CharField(max_length=300, null=True)),
                ('client', models.ForeignKey(limit_choices_to={'is_client': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('service', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='user.service')),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(help_text='Insira número no formato (xx) 98765-4321', max_length=11, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='ceo',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.RESTRICT, related_name='business_ceo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='business',
            name='ceo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='business_ceo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='business',
            name='ceo',
            field=models.OneToOneField(blank=True, default=2, on_delete=django.db.models.deletion.RESTRICT, related_name='business_ceo', to='user.customuser'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='business',
            name='invitations',
            field=models.ManyToManyField(blank=True, related_name='user_invitations', to=settings.AUTH_USER_MODEL),
        ),
    ]
