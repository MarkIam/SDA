# Generated by Django 3.2.8 on 2021-11-28 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manifest', '0005_auto_20211128_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='skydivediscipline',
            name='description',
            field=models.TextField(default='-', max_length=10, verbose_name='Описание дисциплины'),
        ),
        migrations.AddField(
            model_name='skydivediscipline',
            name='short_name',
            field=models.CharField(default='-', max_length=10, verbose_name='Короткое название дисциплины'),
        ),
    ]
