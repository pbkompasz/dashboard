from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserPaymentMethod(models.Model):
  METHODS = (
    ("STRIPE", "Stripe"),
    ("PAYPAL", "PayPal"),
  )
  name = models.CharField(max_length=7, choices=METHODS)
  token = models.CharField(max_length=20)
  belongs_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

class Invoice(models.Model):
  file = models.FileField(upload_to='documents/')
  date_approved = models.DateField()
  date_paid = models.DateField()
