from django import forms
from django.forms import ModelForm

from .models import Product

class UpdateForm(forms.Form):
  name = forms.CharField(label='Name', max_length=100)
  cut_file = forms.FileField(label='Cut file', required=False)
  product_size_width = forms.IntegerField(label='Width')
  product_size_height = forms.IntegerField(label='Height')

class CreateForm(ModelForm):
  class Meta:
    model = Product
    fields = ['name']
  cut_file = forms.FileField(label='Cut file', required=False)
  product_size_width = forms.IntegerField(label='Width')
  product_size_height = forms.IntegerField(label='Height')
