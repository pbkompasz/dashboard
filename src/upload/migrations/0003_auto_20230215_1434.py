# Generated by Django 3.2.17 on 2023-02-15 14:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0001_initial'),
        ('order', '0005_auto_20230215_1311'),
        ('upload', '0002_uploadedfile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Invoice',
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='order.cart'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='payment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='payment.invoice'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='order.status'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='uploadedfile',
            name='belongs_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
