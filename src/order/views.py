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


# TODO Check if Order is in production
def cancel(request):

  if (request.POST):
    return render(request, 'order/index.html')

  return render(request, 'order/index.html')

# TODO Check if Order has not shipped
class OrderUpdateView(DetailView):
  template_name = 'order/update.html'  
  model = Cart

  def post(self, *args, **kwargs):
    # if (not_in_production(1)):
    pass 

