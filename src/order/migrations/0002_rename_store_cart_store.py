# Generated by Django 3.2.17 on 2023-02-14 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='Store',
            new_name='store',
        ),
    ]
