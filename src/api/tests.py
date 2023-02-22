from django.test import TestCase, Client
from django.contrib.auth.models import User

import json

# Create your tests here.

class ApiUploadTests(TestCase):

  def login(self, c):
    c.post('/login/', { 'username': 'admin', 'password': 'admin'})

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

    resp = c.generic('POST', '/api/orders', json.dumps({
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
      ]}))
    print(resp)
    print(resp.content)
    # self.assertEqual(resp.status_code, 400)
    
  def test_known_product_2tshirtsplusone(self):
    """
    Send an empty file
    Should return 400
    """
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
    pass

  def test_known_product_giftbox(self):
    """
    Send an empty file
    Should return 400
    """
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
    pass
  
  def test_unkown_product(self):
    """
    Send an empty file
    Should return 400
    """
    {"carts": [
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
        },
      ]}
    pass

