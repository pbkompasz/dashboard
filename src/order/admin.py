from django.contrib import admin
from .models import Cart, CartItem, CartStatus, Status

# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(CartStatus)
admin.site.register(Status)
