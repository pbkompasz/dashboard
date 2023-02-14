from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListView.as_view(), name='index'),
    path('<int:pk>', views.OrderDetailView.as_view(), name='detail'),
    path('update/<int:pk>', views.OrderUpdateView.as_view(), name='update'),
]