from django import forms
from django.forms import ModelForm

from .models import Cart
 
class UpdateCartForm(ModelForm):
  class Meta:
    model = Cart
    fields = ['client_address', 'client_address_2', 'client_city', 'client_zip', 'client_state']
