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
  date_approved = models.DateField()
  date_paid = models.DateField()
