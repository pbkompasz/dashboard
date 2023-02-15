from django.db import models
from django.contrib.auth.models import User

from order.models import Status, Cart
from payment.models import Invoice

# Create your models here.

class UploadedFile(models.Model):
  date_uploaded = models.DateField()
  file = models.FileField()
  belongs_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
  status = models.ForeignKey(Status, on_delete=models.CASCADE)
  order = models.ForeignKey(Cart, on_delete=models.CASCADE)
  payment = models.ForeignKey(Invoice, on_delete=models.CASCADE)
