from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
  path('orders', login_required(views.JSONDetailView.as_view()), name='orders'),
]