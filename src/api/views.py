from django.shortcuts import render
from django.views.generic.detail import BaseDetailView
from django.views import View
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .mixins import JSONResponseMixin
from upload.models import ApiUpload, Upload, STRUCT
from .serializers import UploadFileSerializer
from order.models import Cart
from payment.models import Invoice

import datetime
import json

# Create your views here.

class JSONDetailView(APIView):
  model = Upload
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request, *args, **kwargs):
    upload_files = Upload.objects.all()
    serializer = UploadFileSerializer(upload_files, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # Create file from data
  def create_file(self, file_name, data):
    pass

  def save_upload(file, data):
    api_upload = ApiUpload(raw=data)
    upload = Upload(
      upload_method='API',
      # file=file,
      # belongs_to = self.request.user,
      # order=order,
      # payment=payment,
      # status=status,
    )
    return upload
  
  def get_value(self, row, attribute):
    # s = next((item for i, item in enumerate(STRUCT) if item['variable_name'] == attribute), None)    
    print(attribute)
    for t in STRUCT:
      if t['variable_name'] == attribute:
        s = t

    print(s)
    for c_name in s['column_names']:
      try:
        return row[c_name]
      except:
        pass
 
  
  # Create UploadFile model
  def create_or_update_orders(self, data, partner):
    new_carts = []
    for d in data:
      # TODO What is store and partner
      cart = Cart.objects.get_or_create(
        store=partner,
        order_number=self.get_value(d, 'order_number'),
        client_address=self.get_value(d, 'client_address'),
        client_address_2=self.get_value(d, 'client_address_2'),
        client_city=self.get_value(d, 'client_city'),
        client_zip=self.get_value(d, 'client_zip'),
        client_state=self.get_value(d, 'client_state'),
        client_email=self.get_value(d, 'client_email'),
        client_phone=self.get_value(d, 'client_phone'),
      )
      cart.save()
      print(cart)
      new_carts.append(cart)
    
    return new_carts

  def get_or_create_invoice(self, orders):
    invoice = None
    return invoice
    for order in orders:
      invoice = Invoice.objects.get(
        order=order,
      )
      break

    if invoice is None:
      # Create invoice
      invoice = Invoice()
      invoice.save()

    for order in orders:
      order.invoice = invoice
      order.save()

    return invoice 
  
  def get_or_create_product(self, data):
    pass

  def create_design(self, data):
    pass

  def post(self, request, *args, **kwargs):
    partner = request.user
    data = {}
    for s in STRUCT:
      data[s['variable_name']] = request.data.get(s['variable_name']) if not None else s['default']
    if not 'orders' in request.data:
      context = {
        'status': '400', 'reason': 'JSON missing \'orders\' attribute', 
      }
      response = Response(context)
      response.status_code = 400
      return response

    orders = self.create_or_update_orders(request.data['orders'], partner)
    invoice = self.get_or_create_invoice(orders)

    context = {
      'ok': 'true',
      'orders': orders,
      'invoice': invoice,
    }
    response = Response(context)
    return response

{
  "orders": [
    {
      "Code":  "123",
      "Product Type": "2TShirtsPlusOnesieSET_1stChristmas",
      "Main design file name (.png)": "main",
      "Dad title image file (.png)": "main_papa",
      "Mom title image file (.png)": "main_mama",
      "Baby’s name (Text)": "main_baby",
      "Dad Tshirt Size": "l",
      "Mom Tshirt Size": "m",
      "Baby’s OneSie Size": "s",
      # Required only for GIFTBOX
      # "Size": "",
      "Shipping Fullname": "John Doe",
      "Phone": "+1 202-918-2132",
      # Optional
      # "order date": "",
      "Email": "me@asd.com",
      "Address1": "291 Reeves Street",
      # Optional
      # "Address2": "",
      "City": "Green Bay",
      "Province": "Wisconsin",
      "Zip": "54301",
      "Country Code": "USA",
      # Not required for 2TShirtsPlusOnesieSET_1stChristmas
      # "UnFulfill Quantity": "",
      # "Printer Design Url Back": "",
      # "Printer Design Url Front": ""
    }
  ]
}

{
  "orders": [
    {
      "Code":  "123",
      "Product Type": "2TShirtsPlusOnesieSET_1stChristmas",
      "Main design file name (.png)": "main",
      "Dad title image file (.png)": "main_papa",
      "Mom title image file (.png)": "main_mama",
      "Baby’s name (Text)": "main_baby",
      "Dad Tshirt Size": "l",
      "Mom Tshirt Size": "m",
      "Baby’s OneSie Size": "s",
      "Shipping Fullname": "John Doe",
      "Phone": "+1 202-918-2132",
      "Email": "me@asd.com",
      "Address1": "291 Reeves Street",
      "City": "Green Bay",
      "Province": "Wisconsin",
      "Zip": "54301",
      "Country Code": "USA"
    }
  ]
}
