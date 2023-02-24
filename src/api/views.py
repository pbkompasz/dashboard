from django.views.generic.detail import BaseDetailView
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .mixins import JSONResponseMixin
from upload.models import Upload, STRUCT
from .models import ApiUpload
from .serializers import UploadFileSerializer
from order.models import Cart
from payment.models import Invoice

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

  def save_upload(self):
    data =  self.request.data
    api_upload = ApiUpload(raw=data)
    api_upload.save() 
    return api_upload
  
  def get_value(self, row, attribute):
    for t in STRUCT:
      if t['variable_name'] == attribute:
        s = t

    for c_name in s['column_names']:
      try:
        return row[c_name]
      except:
        pass
 
  
  # Create UploadFile model
  def create_or_update_cart(self, data, partner):
    new_carts = []
    messages = []
    for d in data:
      valid, message = self.is_row_valid(d)
      if not valid:
        messages.append({'message': message})
      cart, _ = Cart.objects.get_or_create(
        # store=partner,
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
      new_carts.append(cart)
    
    return new_carts, messages

  def get_or_create_invoice(self, carts):
    invoice = {}
    return invoice
    for cart in carts:
      try:
        cart['invoice']
      except:
        if invoice == None:
          invoice = create_invoice()
        cart.invoice = invoice
        cart.save()

    return invoice 
  
  def get_or_create_product(self, data):
    pass

  def create_design(self, data):
    pass

  def is_json_valid(self, data):
    if not 'carts' in self.request.data:
      return False, 'JSON missing \'carts\' attribute'
    return True, None

  def is_row_valid(self, row):
    for s in STRUCT:
      if 'required' in s:
        ok = False
        for name in s['column_names']:
          if name in row:
            ok = True
            break
        if not ok:
          return False, 'Missing required field: ' + s['variable_name']
    return True, None

  def post(self, request, *args, **kwargs):
    partner = request.user
    data = {}
    valid, message = self.is_json_valid(data)
    if not valid:
      context = {
        'status': '400', 'message': message, 
      }
      response = Response(context)
      response.status_code = 400
      return response
    
    self.save_upload()

    carts, messages = self.create_or_update_cart(request.data['carts'], partner)
    invoice = self.get_or_create_invoice(carts)

    context = {
      'ok': 'true',
      'carts': serializers.serialize("json", carts),
      'invoice': serializers.serialize("json", invoice),
      'messages': messages,
    }
    response = Response(data=context)
    return response

{
  "carts": [
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
