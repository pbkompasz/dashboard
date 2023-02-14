from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, views
from django.urls import reverse_lazy
from django.contrib import messages


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
  pass

class SignupView(View):
  template_name = 'index/signup.html'

  def get(self, request, *args, **kwargs):
    form = UserCreationForm()
    return render(request, 'index/signup.html', {'form': form})

  def post(self, request, *args, **kwargs):
    form = UserCreationForm(request.POST)
    print(form)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      raw_password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=raw_password)
      resp = login(request, user)
      print(resp)
      return render(request, 'index/index.html')
    return render(request, 'index/signup.html', {'form': form})

class LoginView(views.LoginView):
  template_name='index/login.html'
  redirect_authenticated_user = True

  def get_success_url(self):
    print('here')
    return reverse_lazy('tasks') 

  def form_invalid(self, form):
    print('invlaid')
    messages.error(self.request,'Invalid username or password')
    return self.render_to_response(self.get_context_data(form=form)) 

# class RegisterView():
#   def get(self):
#     return render(self.request, 'index/register')

#   def post(self, *args, **kwargs):
#       last_book = self.get_queryset().latest('publication_date')
#       # Create user
#       response = HttpResponse(
#           # RFC 1123 date format.
#           headers={'Last-Modified': last_book.publication_date.strftime('%a, %d %b %Y %H:%M:%S GMT')},
#       )
#       return response
