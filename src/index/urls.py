from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', login_required(views.dashboard), name='dashboard'),
    # path('login', views.login, name='login'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', login_required(views.logout), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
]

