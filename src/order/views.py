from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Cart

# Create your views here.

class OrderListView(ListView):
  template_name = 'order/index.html'
  model = Cart

  # def get_queryset(self):
  #   return []



class OrderDetailView(DetailView):
  template_name = 'order/detail.html'
  model = Cart


def detail(request):
  context = {
    order_id,
  }
  return render(request, 'order/detail.html', context)

class OrderUpdateView(DetailView):
  template_name = 'order/update.html'  
  model = Cart
