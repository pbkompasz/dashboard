from django.test import TestCase, Client
from django.contrib.auth.models import User

from order.models import Cart
from catalog.models import Product

import json
from pprint import pprint

# Create your tests here.

class ApiUploadTests(TestCase):

  def test_api_general(self):
    """
    Send an empty file
    Should return 400
    """
    user = User.objects.create(username='testuser')
    user.set_password('12345')
    user.save()

    c = Client()
    logged_in = c.login(username='testuser', password='12345')

    resp = c.post('/api/orders',
      json.dumps({
        "carts": [
          {
            "Code":  "test_api_1",
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
      }),
      content_type="application/json", )
    self.assertEqual(resp.status_code, 200)
    
  def test_known_product_2tshirtsplusone(self):
    """
    Send an empty file
    Should return 400
    """
    user = User.objects.create(username='testuser')
    user.set_password('12345')
    user.save()

    c = Client()
    logged_in = c.login(username='testuser', password='12345')
    data = {
      "carts": [
        {
          "Code":  "test_api_2",
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
          "Country Code": "USA",
          # "Printer Design Url Back": "",
          # "Printer Design Url Front": ""
        }
      ]
    }
    resp = c.post('/api/orders',
      json.dumps(data),
      content_type="application/json", )
    self.assertEqual(resp.status_code, 200)

    try:
      Cart.objects.get(order_number='test_api_2')
    except Exception: 
      self.fail('Cart was not created')

    try:
      Product.objects.get(name='2TShirtsPlusOnesieSET_1stChristmas')
    except Exception: 
      self.fail('Product creation error')

    try:
      Cart.object.get(order_number_internal='test_api_2')
    except Exception: 
      self.fail('Cart was not created')



  def test_known_product_giftbox(self):
    """
    Send an empty file
    Should return 400
    """
    {
      "carts": [
        {
          "Code":  "test_api_3",
          "Product Type": "GIFTBOX",
          "Size": "l",
          "Shipping Fullname": "John Doe",
          "Phone": "+1 202-918-2132",
          "Email": "me@asd.com",
          "Address1": "291 Reeves Street",
          "Address2": "293 Reeves Street",
          "City": "Green Bay",
          "Province": "Wisconsin",
          "Zip": "54301",
          "Country Code": "USA",
          "UnFulfill Quantity": 1,
          # "Printer Design Url Back": "",
          # "Printer Design Url Front": ""
        }
      ]
    }
    pass
  
  def test_unkown_product(self):
    """
    Send an empty file
    Should return 400
    """
    {"carts": [
        {
          "Code":  "test_api_4",
          "Product Type": "My Product",
          "Shipping Fullname": "John Doe",
          "Phone": "+1 202-918-2132",
          "Email": "me@asd.com",
          "Address1": "291 Reeves Street",
          "City": "Green Bay",
          "Province": "Wisconsin",
          "Zip": "54301",
          "Country Code": "USA",
          "UnFulfill Quantity": 2,
          "Printer Design Url Back": "",
          "Printer Design Url Front": ""
        },
      ]}
    pass

