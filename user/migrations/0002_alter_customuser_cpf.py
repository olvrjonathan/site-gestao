# Generated by Django 3.2.5 on 2021-11-25 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='cpf',
            field=models.CharField(max_length=11, null=True),
        ),
    ]
