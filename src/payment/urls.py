from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views
from .views import SetupPaymentMethodView

urlpatterns = [
    path('', login_required(views.PaymentListView.as_view()), name='index'),
    path('<int:pk>', login_required(views.SetupPaymentMethodView.as_view()), name='setup'),
]