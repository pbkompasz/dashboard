from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class ApiUpload(models.Model):
  raw = models.JSONField()

@receiver(post_save, sender=ApiUpload)
def my_handler2(sender, instance, **kwargs):
  from upload.models import Upload
  upload = Upload(
    upload_method = 'API',
    api_upload = instance,
  )
  upload.save()

