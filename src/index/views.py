from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, views, logout as auth_logout
from django.urls import reverse_lazy
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User

from payment.models import UserPaymentMethod

import stripe

# Create your views here.

def is_logged_in(request):
  return request.user.is_authenticated

def index(request):
  if is_logged_in(request):
    return redirect('dashboard')
  return render(request, 'index/index.html')

# @login_required(redirect_field_name='my_redirect_field')
def dashboard(request):
  return render(request, 'index/dashboard.html')

class SignupView(View):
  template_name = 'index/signup.html'

  def get(self, request, *args, **kwargs):
    form = UserCreationForm()
    return render(request, 'index/signup.html', {'form': form})

  def post(self, request, *args, **kwargs):
    form = UserCreationForm(request.POST)
    if form.is_valid():
      stripe.api_key = settings.STRIPE_SECRET_KEY
      customer = stripe.Customer.create()
      form.save()
      username = form.cleaned_data.get('username')
      raw_password = form.cleaned_data.get('password')
      authenticate(username=username, password=raw_password)
      user = User.objects.get(username=username)

      # Create Stripe, Paypal payment methods
      payment_method = UserPaymentMethod(
        belongs_to=user,
        name='STRIPE',
        customer=customer,
      )
      payment_method.save()
      payment_method2 = UserPaymentMethod(
        belongs_to=user,
        name='PayPal',
      )
      payment_method2.save()

      login(request, user)
      return render(request, 'index/index.html')
    else:
      messages.error(request, form.errors)
    return render(request, 'index/signup.html', {'form': form})

class LoginView(views.LoginView):
  template_name='index/login.html'
  redirect_authenticated_user = True

  def get_success_url(self):
    return reverse_lazy('dashboard') 

  def form_invalid(self, form):
    messages.error(self.request,'Invalid username or password')
    return self.render_to_response(self.get_context_data(form=form)) 

class ForgotPasswordView(View):
  template_name = 'index/forgot-password.html'

  def get(self, request, *args, **kwargs):
    return render(request, 'index/forgot-password.html')

def logout(request):

  if (request.method == 'GET'):
    auth_logout(request)
    return redirect('dashboard', )
