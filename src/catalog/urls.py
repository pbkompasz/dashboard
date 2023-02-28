from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'catalog'
urlpatterns = [
    path('', login_required(views.ProductListView.as_view()), name='index'),
    path('create', login_required(views.ProductCreateView.as_view()), name='create'),
    path('<int:pk>', login_required(views.ProductUpdateView.as_view()), name='details'),
    path('<int:pk>/update', login_required(views.ProductUpdateView.as_view()), name='update'),
]