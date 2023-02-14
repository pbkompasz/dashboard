"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls')),
    path('dashboard/catalog/', login_required(include('catalog.urls')), name='catalog'),
    path('dashboard/order/', login_required(include('order.urls')), name='order'),
    # path('dashboard/order/', include('order.urls'), name='order'),
    path('dashboard/payment/', login_required(include('payment.urls')), name='payments'),
    path('dashboard/upload/', login_required(include('upload.urls')), name='upload'),
    # path('', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),

]
