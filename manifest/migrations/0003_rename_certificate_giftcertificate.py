# Generated by Django 3.2.8 on 2021-11-25 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manifest', '0002_auto_20211123_2349'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Certificate',
            new_name='GiftCertificate',
        ),
    ]
