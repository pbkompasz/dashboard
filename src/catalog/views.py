from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from .models import Product

# Create your views here.

class ProductListView(ListView):
  template_name = 'catalog/index.html'
  model = Product

class ProductCreateView(CreateView):
  template_name = 'catalog/create.html'
  model = Product

class ProductUpdateView(UpdateView):
  template_name = 'catalog/update.html'
  model = Product

  # is_private = True
  # has_access = True

  # context = {
  #   'is_private': is_private,
  #   'has_access': has_access,
  # }
  # return render(request, 'catalog/update', context)
