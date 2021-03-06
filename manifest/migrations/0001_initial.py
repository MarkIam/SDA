# Generated by Django 3.2.8 on 2021-11-21 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Skydiver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=64, verbose_name='Фамилия')),
                ('patronymic', models.CharField(max_length=64, verbose_name='Отчество')),
                ('birth_date', models.DateField(verbose_name='Дата рождения')),
                ('passport_number', models.CharField(max_length=10, verbose_name='Серия и номер паспорта')),
                ('passport_data', models.TextField(max_length=256, verbose_name='Кем и когда выдан паспорт')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Электронная почта')),
                ('phone_number', models.CharField(max_length=10, verbose_name='Номер телефона')),
            ],
        ),
    ]
