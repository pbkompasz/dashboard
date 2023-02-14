from django.db import models

# Create your models here.

class UserPaymentMethod(models.Model):
  METHODS = (
    ("STRIPE", "Stripe"),
    ("PAYPAL", "PayPal"),
)
  name = models.CharField(max_length=7, choices=METHODS)
  token = models.CharField(max_length=20)

class Invoice(models.Model):
  file = models.FileField(upload_to='documents/')
  data_approved = models.DateField()
  data_paid = models.DateField()
