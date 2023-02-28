from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views
from .views import SetupPaymentMethodView, PaymentListView

urlpatterns = [
    path('', login_required(PaymentListView.as_view()), name='index'),
    path('<int:pk>', login_required(SetupPaymentMethodView.as_view()), name='setup'),
]