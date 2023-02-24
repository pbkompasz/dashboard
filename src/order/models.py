from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from catalog.models import Product
from payment.models import Invoice

import datetime

# Create your models here.

def pkgen():
  from base64 import b32encode
  from hashlib import sha1
  from random import random
  rude = (b'lol',)
  bad_pk = True
  while bad_pk:
    pk = b32encode(sha1((str(random()).encode())).digest()).lower()[:6]
    bad_pk = False
    for rw in rude:
      if pk.find(rw) >= 0: bad_pk = True
  return pk

class Status(models.Model):
  name = models.CharField(max_length=15)
  color = models.CharField(max_length=10)

class ImageDesign(models.Model):
  stored_data = models.JSONField(),
  image_creator_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True),

class Cart(models.Model):
  store = models.CharField(max_length=15)
  order_number = models.CharField(max_length=25, unique=True)
  order_number_internal = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
  client_address = models.CharField(max_length=50, null=True)
  client_address_2 = models.CharField(max_length=50, null=True)
  client_city = models.CharField(max_length=50, null=True)
  client_zip = models.CharField(max_length=15, null=True)
  client_state = models.CharField(max_length=15, null=True)
  client_email = models.CharField(max_length=20, null=True)
  client_phone = models.CharField(max_length=15, null=True)
  total_cost = models.IntegerField(default=0)
  invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True, null=True)
  date_closed_at = models.DateField(default=datetime.date.today)

  def is_cancellable(self):
    return not self.cartstatus.status.name in ['Cancelled', 'Production', 'Shipped']

  def is_address_updateable(self):
    return not self.cartstatus.status.name in ['Cancelled', 'Shipped']


@receiver(post_save, sender=Cart)
def my_handler(sender, instance, **kwargs):
  status, _ = Status.objects.get_or_create(
    name='Registered',
    color='grey'
  )
  cart_status, _ = CartStatus.objects.get_or_create(
    status=status,
    cart=instance,
  )


class CartItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  qty = models.IntegerField()
  cost = models.IntegerField(null=True)
  image = models.ForeignKey(ImageDesign, on_delete=models.CASCADE),
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  design_1_source = models.ForeignKey(ImageDesign, on_delete=models.CASCADE, null=True)
  front_pdf = models.CharField(max_length=15, default='')
  back_pdf = models.CharField(max_length=15, default='')

@receiver(post_save, sender=CartItem)
def my_handler(sender, instance, **kwargs):
  cart = Cart.objects.get(order_number_internal=instance.cart.order_number_internal)
  cost = 0
  for ci in cart.cartitem_set.all():
    if not ci.cost == None:
      cost += ci.cost
  cart.total_cost = cost
  cart.save()

class CartStatus(models.Model):
  status = models.ForeignKey(Status, on_delete=models.CASCADE)
  current = models.BooleanField(default = False)
  date_started = models.DateField(default=datetime.date.today)
  date_completed = models.DateField(blank=True, null=True)
  cart = models.OneToOneField(
    Cart,
    on_delete=models.CASCADE,
  )
