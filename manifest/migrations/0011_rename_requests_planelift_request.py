# Generated by Django 3.2.8 on 2021-12-04 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manifest', '0010_auto_20211202_1615'),
    ]

    operations = [
        migrations.RenameField(
            model_name='planelift',
            old_name='requests',
            new_name='request',
        ),
    ]
