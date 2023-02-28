from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', login_required(views.OrderListView.as_view()), name='index'),
    path('<int:pk>', login_required(views.OrderDetailView.as_view()), name='details'),
    path('<int:pk>/update', login_required(views.OrderUpdateView.as_view()), name='update'),
    path('<int:pk>/cancel', login_required(views.cancel), name='cancel_order'),
]