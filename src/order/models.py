from django.db import models
import datetime

from django.contrib.auth.models import User
from catalog.models import Product
from payment.models import Invoice

# Create your models here.

def pkgen():
  from base64 import b32encode
  from hashlib import sha1
  from random import random
  rude = ('lol',)
  bad_pk = True
  while bad_pk:
    pk = b32encode(sha1(str(random())).digest()).lower()[:6]
    bad_pk = False
    for rw in rude:
      if pk.find(rw) >= 0: bad_pk = True
  return pk

class Status(models.Model):
  name = models.CharField(max_length=7)
  color = models.CharField(max_length=10)

class ImageDesign(models.Model):
  stored_data = models.JSONField(),
  image_creator_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True),

class Cart(models.Model):
  store = models.CharField(max_length=15)
  order_number = models.IntegerField()
  order_number_internal = models.CharField(max_length=6, primary_key=True, default=pkgen)
  client_address = models.CharField(max_length=50, null=True)
  client_address_2 = models.CharField(max_length=50, null=True)
  client_city = models.CharField(max_length=50, null=True)
  client_zip = models.CharField(max_length=10, null=True)
  client_state = models.CharField(max_length=15, null=True)
  client_email = models.CharField(max_length=20, null=True)
  client_phone = models.CharField(max_length=10, null=True)
  total_cost = models.IntegerField(default=0)
  invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True, null=True)
  date_closed_at = models.DateField(default=datetime.date.today)

  def create_order(self, data):
    print(data)

class CartItem(models.Model):
  product = models.ManyToManyField(Product)
  product_size = models.IntegerField()
  quantity = models.IntegerField()
  cost = models.IntegerField()
  image = models.ForeignKey(ImageDesign, on_delete=models.CASCADE),
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  design_1_source = models.ForeignKey(ImageDesign, on_delete=models.CASCADE)
  front_pdf = models.CharField(max_length=15, default='')
  back_pdf = models.CharField(max_length=15, default='')

class CartStatus(models.Model):
  status = models.ForeignKey(Status, on_delete=models.CASCADE)
  current = models.BooleanField(default = False)
  date_started = models.DateField(default=datetime.date.today)
  date_completed = models.DateField(blank=True, null=True)
  cart = models.OneToOneField(
    Cart,
    on_delete=models.CASCADE,
  )
