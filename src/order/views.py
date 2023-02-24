from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.urls import reverse
from django.contrib import messages

from .models import Cart, CartItem, Status
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

def cancel(request, pk):
  if (request.POST):
    print(pk)
    try:
      cart = Cart.objects.get(order_number_internal=pk)
      if cart.is_cancellable():
        cancelled_status, _ = Status.objects.get_or_create(
          name='Cancelled'
        )
        cart.cartstatus.status = cancelled_status
        cart.cartstatus.save()
      else:
        print('Order already shipped/in production')
        messages.error(request,'Order shipped/in production')
    except Exception as e:
      print(e)
      return redirect(reverse('detail', kwargs={'pk': pk}))
    return redirect(reverse('detail', kwargs={'pk': pk}))

  messages.error(request,'Order shipped/in production')

  return render(request, 'order/index.html')

class OrderUpdateView(DetailView):
  template_name = 'order/update.html'  
  model = Cart

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['form'] = UpdateCartForm(instance=self.object)
    return context


  def post(self, *args, **kwargs):
    try:
      cart = Cart.objects.get(order_number_internal=self.kwargs['pk'])
      if cart.is_address_updateable():
        form = self.request.POST
        cart.client_address = form['client_address']
        cart.client_address_2 = form['client_address_2']
        cart.client_city = form['client_city']
        cart.client_zip = form['client_zip']
        cart.client_state = form['client_state']
        cart.save()
      else:
        print('Order already shipped')
        messages.error(self.request,'Order already shipped')
      return redirect(reverse('detail', kwargs={'pk': self.kwargs['pk']}))
    except Exception as e:
      print(e)
      messages.error(self.request, 'Some error')
    return render(self.request, reverse('index'))