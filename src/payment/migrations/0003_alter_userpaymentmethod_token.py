# Generated by Django 3.2.18 on 2023-02-23 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_userpaymentmethod_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpaymentmethod',
            name='token',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
