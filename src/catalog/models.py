from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProductSize(models.Model):
  width = models.IntegerField()
  height = models.IntegerField()

class Product(models.Model):
  name = models.CharField(max_length=50)
  type = models.CharField(max_length=10, default='global')
  cut_file = models.FileField(upload_to='documents/')
  belongs_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
  product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, null=True)

  def is_private(self):
    return self.belongs_to is not None
