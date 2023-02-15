from django.db import models
import datetime
from catalog.models import Product
from payment.models import Invoice

# Create your models here.

class Status(models.Model):
  name = models.CharField(max_length=7)
  color = models.CharField(max_length=10)

class CartItem(models.Model):
  product = models.ManyToManyField(Product)
  product_size = models.IntegerField()
  quantity = models.IntegerField()
  cost = models.IntegerField()
  # image = models.ImageField()

class Cart(models.Model):
  store = models.CharField(max_length=15)
  order_number = models.IntegerField()
  order_number_internal = models.IntegerField()
  client_address = models.CharField(max_length=50)
  client_address_2 = models.CharField(max_length=50)
  client_city = models.CharField(max_length=50)
  client_zip = models.CharField(max_length=10)
  client_state = models.CharField(max_length=15)
  client_email = models.CharField(max_length=20)
  client_phone = models.CharField(max_length=10)
  total_cost = models.IntegerField()
  invoice = models.OneToOneField(
    Invoice,
    on_delete=models.CASCADE,
    blank=True, null=True
  )

  def create_order(self, data):
    print(data)

class CartStatus(models.Model):
  status = models.ForeignKey(Status, on_delete=models.CASCADE)
  current = models.BooleanField(default = False)
  date_started = models.DateField(default=datetime.date.today)
  date_completed = models.DateField(blank=True, null=True)
  cart = models.OneToOneField(
    Cart,
    on_delete=models.CASCADE,
  )
