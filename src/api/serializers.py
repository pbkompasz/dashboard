from rest_framework import serializers

from upload.models import Upload

class UploadFileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Upload
    fields = ["date_uploaded", "cart", 'api_upload']

class CreateCartSerializer(serializers.ModelSerializer):
  class Meta:
    model = Upload
    fields = ["date_uploaded", "cart", 'api_upload']
