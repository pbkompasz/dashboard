from django.contrib import admin

from .models import Invoice, UserPaymentMethod
# Register your models here.

admin.site.register(Invoice)
admin.site.register(UserPaymentMethod)
