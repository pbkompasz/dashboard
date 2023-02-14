from django.db import models

# Create your models here.

class Invoice(models.Model):
  # file = 
  date_approved = models.DateField()
  date_paid = models.DateField()
