# Generated by Django 3.2.17 on 2023-02-15 20:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0001_initial'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_uploaded', models.DateField()),
                ('file', models.FileField(upload_to='')),
                ('belongs_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.cart')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.invoice')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.status')),
            ],
        ),
    ]
