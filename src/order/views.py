from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Cart, CartItem
from .forms import UpdateCartForm

# Create your views here.

class OrderListView(ListView):
  template_name = 'order/index.html'
  model = Cart

  # def get_queryset(self):
  #   return []


from pprint import pprint

class OrderDetailView(DetailView):
  template_name = 'order/detail.html'
  model = Cart

  def get_context_data(self, *args, **kwargs):
    ctx = super().get_context_data(*args, **kwargs)
    ctx['cartitems'] = CartItem.objects.all().filter(cart=self.object)
    return ctx


# TODO Check if Order is in production
def cancel(request):

  if (request.POST):
    return render(request, 'order/index.html')

  return render(request, 'order/index.html')

# TODO Check if Order has not shipped
class OrderUpdateView(DetailView):
  template_name = 'order/update.html'  
  model = Cart

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['form'] = UpdateCartForm(instance=self.object)
    return context


  def post(self, *args, **kwargs):
    # if (not_in_production(1)):
    pass 

