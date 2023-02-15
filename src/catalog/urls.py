from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),
    path('create', views.ProductCreateView.as_view(), name='create'),
    path('<int:pk>/update', views.ProductUpdateView.as_view(), name='update'),
]