from django.urls import path
from . import views

urlpatterns = [
    path('', views.UploadIndexView.as_view(), name='index'),
]
