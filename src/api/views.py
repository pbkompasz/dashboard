from django.shortcuts import render
from django.views.generic.detail import BaseDetailView
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .mixins import JSONResponseMixin
from upload.models import UploadedFile, STRUCT
from .serializers import UploadFileSerializer
from order.models import Status

import datetime

# Create your views here.

class JSONDetailView(APIView):
  model = UploadedFile
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request, *args, **kwargs):
    upload_files = UploadedFile.objects.all()
    serializer = UploadFileSerializer(upload_files, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # Create file from data
  def create_file(self, file_name, data):
    pass
  
  # Create UploadFile model
  def save_file(self, data):
    date = datetime.now()
    date_str = date.strftime('%m/%d/%Y')
    # file = create_file(f'{self.request.user}-{date}', data)
    # order, payment, status = create_order()
    uploaded_file = UploadedFile(
      date_uploaded=date,
      # file=file,
      belongs_to = self.request.user,
      # order=order,
      # payment=payment,
      # status=status,
    )
  def post(self, request, *args, **kwargs):
    print(request.data)
    data = {}
    for s in STRUCT:
      data[s['variable_name']]: request.data.get(s['variable_name'])



    serializer = UploadFileSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)