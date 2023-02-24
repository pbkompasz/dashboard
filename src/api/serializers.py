from rest_framework import serializers

from upload.models import Upload

class UploadFileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Upload
    fields = ["date_uploaded", 'api_upload', 'file_upload']

class CreateOrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = Upload
    fields = ["date_uploaded", "order", 'api_upload']
