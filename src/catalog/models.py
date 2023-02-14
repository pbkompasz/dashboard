from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
  name = models.CharField(max_length=25)
  type = models.CharField(max_length=10, default='global')
  cut_file = models.FileField(upload_to='documents/')
  belongs_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

class ProductSize(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  width = models.IntegerField()
  height = models.IntegerField()
