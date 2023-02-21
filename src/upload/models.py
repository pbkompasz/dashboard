from django.db import models
from django.contrib.auth.models import User

from order.models import Status, Cart
from payment.models import Invoice

import datetime

# Create your models here.

STRUCT = [
  {
    'variable_name': 'order_number',
    'column_names': ['Code', 'code'],
    'default': None,
    'required': True,
  }, {
    'variable_name': 'product',
    'column_names': ['Product Type', 'SKU'],
    'default': None,
    'required': True,
  }, {
    'variable_name': 'designx',
    'column_names': ['Main design file name (.png)'],
    'default': None,
  }, {
    'variable_name': 'designd',
    'column_names': ['Dad title image file (.png)'],
    'default': None,
  }, {
    'variable_name': 'designm',
    'column_names': ['Mom title image file (.png)'],
    'default': None,
  }, {
    'variable_name': 'designb',
    'column_names': ["Baby's name (Text)", "Baby’s name (Text)", "Baby`s name (Text)"],
    'default': None,
  }, {
    'variable_name': 'papa',
    'column_names': ['Dad Tshirt Size'],
    'default': None,
  }, {
    'variable_name': 'mama',
    'column_names': ['Mom Tshirt Size'],
    'default': None,
  }, {
    'variable_name': 'baby',
    'column_names': ["Baby's OneSie Size", "Baby’s OneSie Size", "Baby`s OneSie Size"],
    'default': None,
  }, {
    'variable_name': 'variant',
    'column_names': ['size', 'Size'],
    'default': None,
  }, {
    'variable_name': 'client_full_name',
    'column_names': ['Shipping Fullname'],
    'default': None,
    'required': True,
  }, {
    'variable_name': 'client_phone',
    'column_names': ['Phone'],
    'default': None,
    'required': True,
  }, {
    'variable_name': 'date_completed',
    'column_names': ['order date'],
    'default': "",
  }, {
    'variable_name': 'client_email',
    'column_names': ['Email'],
    'default': None,
    'required': True,
  }, {
    'variable_name': 'client_address',
    'column_names': ['Address1'],
    'default': None,
    'required': True,
  }, {
    'variable_name': 'client_address_2',
    'column_names': ['Address2'],
    'default': None,
  }, {
    'variable_name': 'client_city',
    'column_names': ['City'],
    'default': None,
    'required': True,
  }, {
    'variable_name': 'client_state',
    'column_names': ['Province'],
    'default': None,
    'required': True,
  }, {
    'variable_name': 'client_zip',
    'column_names': ['Zip'],
    'default': None,
    'required': True,
  }, {
    'variable_name': 'client_country',
    'column_names': ['Country Code'],
    'default': None,
    'required': True,
  }, {
    'variable_name': 'qty',
    'column_names': ['UnFulfill Quantity', 'Qty'],
    'default': None,
  }, {
    'variable_name': 'frurla',
    'column_names': ['Printer Design Url Front'],
    'default': None,
  }, {
    'variable_name': 'brurla',
    'column_names': ['Printer Design Url Back'],
    'default': None,
  },
]

class ApiUpload(models.Model):
  raw = models.JSONField()

class FileUpload(models.Model):
  file = models.FileField()

class Upload(models.Model):
  # belongs_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
  # status = models.ForeignKey(Status, on_delete=models.CASCADE)
  # ManyToMany
  # payment = models.ForeignKey(Invoice, on_delete=models.CASCADE)
  UPLOAD_METHOD_CHOICES = (
    ("MANUAL", "manual"),
    ("API", "api"),
  )
  upload_method = models.CharField(max_length=7, choices=UPLOAD_METHOD_CHOICES)
  date_uploaded = models.DateField(default=datetime.date.today)
  order = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
  file_upload = models.OneToOneField(FileUpload, on_delete=models.CASCADE)
  api_upload = models.OneToOneField(ApiUpload, on_delete=models.CASCADE)
