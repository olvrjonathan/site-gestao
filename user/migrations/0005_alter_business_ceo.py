# Generated by Django 3.2.5 on 2021-12-02 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_business_invitations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='ceo',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.RESTRICT, related_name='business_ceo', to=settings.AUTH_USER_MODEL),
        ),
    ]