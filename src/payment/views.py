from django.shortcuts import render
from django.views.generic import ListView

from .models import Invoice, UserPaymentMethod

# Create your views here.

class PaymentListView(ListView):
  model = Invoice
  template_name = 'payment/index.html'

  def get_context_data(self, *args, **kwargs):
    context = super(PaymentListView, self).get_context_data(*args, **kwargs)
    context['invoices_paid'] = Invoice.objects.exclude(
      date_paid = None )
    context['payment_methods'] = UserPaymentMethod.objects.all()
    return context
