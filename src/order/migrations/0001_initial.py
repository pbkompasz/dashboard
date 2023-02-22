# Generated by Django 3.2.18 on 2023-02-22 20:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('order_number_internal', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('store', models.CharField(max_length=15)),
                ('order_number', models.CharField(max_length=25, unique=True)),
                ('client_address', models.CharField(max_length=50, null=True)),
                ('client_address_2', models.CharField(max_length=50, null=True)),
                ('client_city', models.CharField(max_length=50, null=True)),
                ('client_zip', models.CharField(max_length=15, null=True)),
                ('client_state', models.CharField(max_length=15, null=True)),
                ('client_email', models.CharField(max_length=20, null=True)),
                ('client_phone', models.CharField(max_length=15, null=True)),
                ('total_cost', models.IntegerField(default=0)),
                ('date_closed_at', models.DateField(default=datetime.date.today)),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.invoice')),
            ],
        ),
        migrations.CreateModel(
            name='ImageDesign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('color', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='CartStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current', models.BooleanField(default=False)),
                ('date_started', models.DateField(default=datetime.date.today)),
                ('date_completed', models.DateField(blank=True, null=True)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='order.cart')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.status')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('cost', models.IntegerField(null=True)),
                ('front_pdf', models.CharField(default='', max_length=15)),
                ('back_pdf', models.CharField(default='', max_length=15)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.cart')),
                ('design_1_source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='order.imagedesign')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product')),
            ],
        ),
    ]
