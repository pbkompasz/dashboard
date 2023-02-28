from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View
from django.conf import settings

from .models import Invoice, UserPaymentMethod
from .forms import AddPaymentForm

import stripe

# Create your views here.

class PaymentListView(ListView):
  model = Invoice
  template_name = 'payment/index.html'

  def get_context_data(self, *args, **kwargs):
    context = super(PaymentListView, self).get_context_data(*args, **kwargs)
    context['invoices_paid'] = Invoice.objects.exclude(
      date_paid = None
        )
    context['payment_methods'] = UserPaymentMethod.objects.all()
    context['form'] = AddPaymentForm()
    # payment_method = UserPaymentMethod.objects.get(belongs_to=self.request.user)
    # stripe.api_key = settings.STRIPE_SECRET_KEY
    # list = stripe.PaymentMethod.list(
    #   customer=payment_method.customer['id'],
    #   # type="card",
    # )
    # if len(list.data) > 0:
    #   payment_method.token = list.data[0].id
    #   payment_method.save()
    
    return context

class SetupPaymentMethodView(DetailView):
  template_name = 'payment/setup.html'
  model = UserPaymentMethod

  def get_context_data(self, *args, **kwargs):
    context = super(SetupPaymentMethodView, self).get_context_data(*args, **kwargs)
    payment_method = UserPaymentMethod.objects.get(belongs_to=self.request.user)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
      customer=payment_method.customer['id'],
      setup_future_usage='on_session',
      amount=1000,
      currency='usd',
      payment_method_options={
        'card': {
          'setup_future_usage': 'off_session',
        },
      },
    )
    context['client_secret']=intent.client_secret
    context['stripe_account']=payment_method.customer['id']
    context['published_key']=settings.STRIPE_PUBLISHABLE_KEY

    return context
