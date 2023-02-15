# Generated by Django 3.2.17 on 2023-02-15 20:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='documents/')),
                ('date_approved', models.DateField()),
                ('date_paid', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='UserPaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('STRIPE', 'Stripe'), ('PAYPAL', 'PayPal')], max_length=7)),
                ('token', models.CharField(max_length=20)),
                ('belongs_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
