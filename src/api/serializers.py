from rest_framework import serializers

from upload.models import UploadedFile

class UploadFileSerializer(serializers.ModelSerializer):
  class Meta:
    model = UploadedFile
    fields = ["date_uploaded", "file", "belongs_to", "status", "order", "payment"]
