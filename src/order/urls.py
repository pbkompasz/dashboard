from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListView.as_view(), name='index'),
    path('<int:pk>', views.OrderDetailView.as_view(), name='detail'),
    path('<int:pk>/update', views.OrderUpdateView.as_view(), name='update'),
    path('<int:pk>/cancel', views.cancel, name='cancel_order'),
]