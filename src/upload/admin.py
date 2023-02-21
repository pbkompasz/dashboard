from django.contrib import admin
from .models import FileUpload, ApiUpload, Upload

# Register your models here.

admin.site.register(Upload)
admin.site.register(ApiUpload)
admin.site.register(FileUpload)
