# Generated by Django 3.2.8 on 2021-11-28 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manifest', '0006_auto_20211128_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skydivediscipline',
            name='description',
            field=models.TextField(default='-', max_length=1000, verbose_name='Описание дисциплины'),
        ),
    ]