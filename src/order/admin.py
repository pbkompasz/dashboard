from django.contrib import admin
from .models import Cart, CartItem, CartStatus, Status, ImageDesign

# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(CartStatus)
admin.site.register(Status)
admin.site.register(ImageDesign)
