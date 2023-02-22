from django.test import TestCase, Client
from django.contrib.auth.models import User

from payment.models import Invoice
from order.models import Cart, CartStatus, ImageDesign, Product
from .models import FileUpload, Upload

import os

# Create your tests here.

class FileUploadTests(TestCase):

  def login(self, c):
    c.post('/login/', { 'username': 'admin', 'password': 'admin'})

  def test_empty_file(self):
    """
    Send an empty file
    Should return 400
    """
    user = User.objects.create(username='testuser')
    user.set_password('12345')
    user.save()

    c = Client()
    logged_in = c.login(username='testuser', password='12345')

    file_path = os.path.join(os.path.dirname(__file__), "test/empty.csv")
    with open(file_path) as fp:
      resp = c.post('/dashboard/upload/', {'file': fp})
      self.assertEqual(resp.status_code, 400)



  def test_file_with_header(self):
    """
    Send a file with only header
    Returns 200
    Doesn't create payment, carts, products or image_designs
    """
    user = User.objects.create(username='testuser')
    user.set_password('12345')
    user.save()

    c = Client()
    logged_in = c.login(username='testuser', password='12345')

    len_cart = len(Cart.objects.all())
    len_cart_status = len(CartStatus.objects.all())
    len_image_design = len(ImageDesign.objects.all())
    len_product = len(Product.objects.all())
    len_upload = len(Upload.objects.all())
    len_file_upload = len(FileUpload.objects.all())
    len_invoice = len(Invoice.objects.all())

    file_path = os.path.join(os.path.dirname(__file__), "test/header.csv")
    with open(file_path) as fp:
      resp = c.post('/dashboard/upload/', {'file': fp})
      self.assertEqual(resp.status_code, 302)
      self.assertEqual(len_cart, len(Cart.objects.all()))
      self.assertEqual(len_cart_status, len(CartStatus.objects.all()))
      self.assertEqual(len_image_design, len(ImageDesign.objects.all()))
      self.assertEqual(len_product, len(Product.objects.all()))
      self.assertEqual(len_invoice, len(Invoice.objects.all()))
      self.assertEqual(len_file_upload+1, len(FileUpload.objects.all()))
      self.assertEqual(len_upload+1, len(Upload.objects.all()))
    

  def test_file_with_one_row_and_new_cart(self):
    """
    File with one row, cart_id is unique
    Should create one payment and cart
    Return 302
    """
    user = User.objects.create(username='testuser')
    user.set_password('12345')
    user.save()

    c = Client()
    logged_in = c.login(username='testuser', password='12345')

    cart_id = 'test_id'
    try:
      cart = Cart.objects.get(id=cart_id)
      self.fail('Cart already exists')
    except:
      pass
    len_cart = len(Cart.objects.all())
    len_cart_status = len(CartStatus.objects.all())
    len_image_design = len(ImageDesign.objects.all())
    len_product = len(Product.objects.all())
    len_invoice = len(Invoice.objects.all())
    len_upload = len(Upload.objects.all())
    len_file_upload = len(FileUpload.objects.all())

    file_path = os.path.join(os.path.dirname(__file__), "test/one_row_new.csv")
    with open(file_path) as fp:
      resp = c.post('/dashboard/upload/', {'file': fp})
      self.assertEqual(resp.status_code, 302)
      self.assertEqual(len(Cart.objects.all()) - len_cart, 1)
      self.assertEqual(len(CartStatus.objects.all()) - len_cart_status, 1)
      self.assertEqual(len_image_design, len(ImageDesign.objects.all()))
      self.assertEqual(len(Product.objects.all()) - len_product, 1)
      self.assertEqual(len(Invoice.objects.all()) - len_invoice, 1)
      self.assertEqual(len(FileUpload.objects.all()) - len_file_upload, 1)
      self.assertEqual(len(Upload.objects.all()) - len_upload, 1)


  def test_file_with_one_row_and_update_cart(self):
    """
    File with one row, cart already exists
    Should create a payment
    Return 302
    """
    user = User.objects.create(username='testuser')
    user.set_password('12345')
    user.save()

    c = Client()
    logged_in = c.login(username='testuser', password='12345')

    cart_id = 'test_id'
    cart = Cart.objects.get_or_create(
      order_number=cart_id,
      # client_full_name="John Doe",
      client_phone="+1 202-918-2132",
      client_email="me@asd.com",
      client_address="291 Reeves Street",
      client_city="Green Bay",
      client_state="Wisconsin",
      client_zip="54301",
      # client_country="USA"
    )
    len_cart = len(Cart.objects.all())
    len_cart_status = len(CartStatus.objects.all())
    len_image_design = len(ImageDesign.objects.all())
    len_product = len(Product.objects.all())
    len_invoice = len(Invoice.objects.all())
    len_upload = len(Upload.objects.all())
    len_file_upload = len(FileUpload.objects.all())

    file_path = os.path.join(os.path.dirname(__file__), "test/one_row_new.csv")
    with open(file_path) as fp:
      resp = c.post('/dashboard/upload/', {'file': fp})
      self.assertEqual(resp.status_code, 302)
      self.assertEqual(len(Cart.objects.all()), len_cart)
      self.assertEqual(len(CartStatus.objects.all()), len_cart_status)
      self.assertEqual(len_image_design, len(ImageDesign.objects.all()))
      # self.assertEqual(len(Product.objects.all()) - len_product, 1)
      self.assertEqual(len(Invoice.objects.all()) - len_invoice, 1)
      self.assertEqual(len(FileUpload.objects.all()) - len_file_upload, 1)
      self.assertEqual(len(Upload.objects.all()) - len_upload, 1)



  def test_file_with_multiple_rows_and_new_carts(self):
    """
    File with one 'lines' row
    Should create one payment and 'lines' cart(s)
    Return 302
    """
    user = User.objects.create(username='testuser')
    user.set_password('12345')
    user.save()

    c = Client()
    logged_in = c.login(username='testuser', password='12345')

    lines = 3 
    len_cart = len(Cart.objects.all())
    len_cart_status = len(CartStatus.objects.all())
    len_image_design = len(ImageDesign.objects.all())
    len_product = len(Product.objects.all())
    len_invoice = len(Invoice.objects.all())
    len_upload = len(Upload.objects.all())
    len_file_upload = len(FileUpload.objects.all())

    file_path = os.path.join(os.path.dirname(__file__), "test/multiple_rows_new.csv")
    with open(file_path) as fp:
      resp = c.post('/dashboard/upload/', {'file': fp})
      self.assertEqual(resp.status_code, 302)
      self.assertEqual(len(Cart.objects.all()) - len_cart, lines)
      self.assertEqual(len(CartStatus.objects.all()) - len_cart_status, lines)
      self.assertEqual(len(Invoice.objects.all()) - len_invoice, 1)
      self.assertEqual(len(FileUpload.objects.all()) - len_file_upload, lines)
      self.assertEqual(len(Upload.objects.all()) - len_upload, lines)



  # def test_file_with_multiple_rows_and_existing_carts(self):
  #   """
  #   was_published_recently() returns False for questions whose pub_date
  #   is in the future.
  #   """
  #   time = timezone.now() + datetime.timedelta(days=30)
  #   future_question = Question(pub_date=time)
  #   self.assertIs(future_question.was_published_recently(), False)


  # def test_file_with_multiple_rows_and_mix_carts(self):
  #   """
  #   was_published_recently() returns False for questions whose pub_date
  #   is in the future.
  #   """
  #   time = timezone.now() + datetime.timedelta(days=30)
  #   future_question = Question(pub_date=time)
  #   self.assertIs(future_question.was_published_recently(), False)
