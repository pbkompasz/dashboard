from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save

from order.models import Status, Cart, Product, CartItem, ImageDesign, CartStatus
from payment.models import Invoice
from api.models import ApiUpload

import datetime
import csv

# Create your models here.

STRUCT = [
  {
    'variable_name': 'order_number',
    'column_names': ['Code', 'code'],
    'required': True,
  }, {
    'variable_name': 'product',
    'column_names': ['Product Type', 'SKU'],
    'required': True,
  }, {
    'variable_name': 'designx',
    'column_names': ['Main design file name (.png)'],
    'default': None,
  }, {
    'variable_name': 'designd',
    'column_names': ['Dad title image file (.png)'],
    'default': None,
  }, {
    'variable_name': 'designm',
    'column_names': ['Mom title image file (.png)'],
    'default': None,
  }, {
    'variable_name': 'designb',
    'column_names': ["Baby's name (Text)", "Baby’s name (Text)", "Baby`s name (Text)"],
    'default': None,
  }, {
    'variable_name': 'papa',
    'column_names': ['Dad Tshirt Size'],
    'default': None,
  }, {
    'variable_name': 'mama',
    'column_names': ['Mom Tshirt Size'],
    'default': None,
  }, {
    'variable_name': 'baby',
    'column_names': ["Baby's OneSie Size", "Baby’s OneSie Size", "Baby`s OneSie Size"],
    'default': None,
  }, {
    'variable_name': 'variant',
    'column_names': ['size', 'Size'],
    'default': None,
  }, {
    'variable_name': 'client_full_name',
    'column_names': ['Shipping Fullname'],
    'required': True,
  }, {
    'variable_name': 'client_phone',
    'column_names': ['Phone'],
    'required': True,
  }, {
    'variable_name': 'date_completed',
    'column_names': ['order date'],
    'default': "",
  }, {
    'variable_name': 'client_email',
    'column_names': ['Email'],
    'required': True,
  }, {
    'variable_name': 'client_address',
    'column_names': ['Address1'],
    'required': True,
  }, {
    'variable_name': 'client_address_2',
    'column_names': ['Address2'],
    'default': None,
  }, {
    'variable_name': 'client_city',
    'column_names': ['City'],
    'required': True,
  }, {
    'variable_name': 'client_state',
    'column_names': ['Province'],
    'required': True,
  }, {
    'variable_name': 'client_zip',
    'column_names': ['Zip'],
    'required': True,
  }, {
    'variable_name': 'client_country',
    'column_names': ['Country Code'],
    'required': True,
  }, {
    'variable_name': 'qty',
    'column_names': ['UnFulfill Quantity', 'Qty'],
    'required': True,
  }, {
    'variable_name': 'frurla',
    'column_names': ['Printer Design Url Front'],
    'default': None,
  }, {
    'variable_name': 'brurla',
    'column_names': ['Printer Design Url Back'],
    'default': None,
  },
]

class FileUpload(models.Model):
  file = models.FileField()

  # Return value or default if missing
  def get_value_for_column_name(self, column_name):
    pass
  
  def process_csv_header(self, csv_file):
    reader = csv.reader(csv_file, delimiter=';')
    first_row = next(reader)
    header_descriptor = {}

    try:
      order_number = first_row.index('Code')
    except:
      reader = csv.reader(csv_file, delimiter=',')
      first_row = next(reader)
      try:
        order_number = first_row.index('Code')
      except:
        print('Missing order number')
        # Return
      
    header_descriptor['order_number'] = order_number 
      
    for s in STRUCT: 
      pos = None
      for c_name in s['column_names']:
        try:
          pos = first_row.index(c_name)
          break
        except:
          pass
      if ((pos is None) or (pos is '')) and (s['required']):
        print('Missing required column')
        raise Exception("Missing required field" + str(s['variable_name']))
        
      header_descriptor[s['variable_name']] = pos if pos is (not None) or not '' else s['default']

    return header_descriptor

  def row_valid(self, row, header_descriptor):
    pass

  def process_csv_body(self, csv_file, header_descriptor, partner, request):
    print('Process body')

    new_carts = []
    old_carts = []
    sizing_chart = {
      'Small': 8,
      'Medium': 9,
      'Large': 10,
      'X-Large': 11,
      '2XL': 12,
      '3XL': 6,
      '4XL': 14
    }
    sizing_baby = {
      '0-3 Meses': 57,
      '3-6 Meses': 58,
      '6-9 Meses': 59,
      '9-12 Meses': 935,
      '12 Meses': 60,
      '18 Meses': 61,
      '24 Meses': 62
    }

    # Init reader
    reader = csv.reader(csv_file, delimiter=';')
    t = next(reader)
    if len(t) <= 1:
      reader = csv.reader(csv_file, delimiter=',')
      next(reader)


    # For every row create a cart
    # The cart has the same 'payment'
    for row in reader:
      cart, created = self.create_cart(row, header_descriptor, partner)
      
      for s in STRUCT:
        try:
          s['required']
        except:
          continue
        if ((row[header_descriptor[s['variable_name']]]) is "" or None) and s['required']:
          print('Missing required value ' + str(s['variable_name']))
          raise Exception("Missing required value " + str(s['variable_name']))

      if created:
        # Link cart to invoice
        # cart.invoice = invoice
        new_carts.append(cart)
      else:
        if cart not in new_carts:
          messages.add_message(
            # TODO
            # self.request, messages.INFO, 'Cart #%s' % cart.friendly_id)
            request, messages.INFO, 'Cart #%s' % cart.order_number)
          old_carts.append(cart)

      if cart in new_carts or created:
        print('here')
        # cart.current_status = CartStatus.objects.create(
        #   cart=cart, status_id=36)
        pd, created = Product.objects.get_or_create(
          # store_id=10,
          name=row[header_descriptor['product']])
        if created:
          messages.add_message(
            request, messages.INFO, 'New Product #%s' % pd.id)
        if created:
          send_mail(
            subject='New Gossby Product',
            message='New Gossby Product - %s' % pd.id,
            from_email='info@mayamedia.io', recipient_list=['info@mayamedia.io'], fail_silently=True
          )
        # if header_descriptor['variant']:
          # Not required
          # pv, created = ProductVariant.objects.get_or_create(
          #   product=pd, name=row[header_descriptor['variant']])
          # if created:
          #   send_mail(
          #     subject='New Gossby Product - Variant',
          #     message='New Gossby Product - %s' % pv.id,
          #     from_email='info@mayamedia.io', recipient_list=['info@mayamedia.io'], fail_silently=True
          #   )

        # Not required
        # parent_po, created = Printable.objects.get_or_create(
        #   title='_'.join(row[header_descriptor['product']].split('_')[:-1]))
        # 
        # if created:
        #   send_mail(
        #     subject='New Gossby Printable',
        #     message='New Gossby Product - %s' % parent_po.id,
        #     from_email='info@mayamedia.io', recipient_list=['info@mayamedia.io'], fail_silently=True
        #   )

        # Not required
        # try:
        #   po, created = PrintableOption.objects.get_or_create(
        #     size_display=row[header_descriptor['variant']], parent=parent_po)
        #   if created:
        #     send_mail(
        #       subject='New Gossby Product - PrintableOption',
        #       message='New Gossby Product - %s' % po.id,
        #       from_email='info@mayamedia.io', recipient_list=['info@mayamedia.io'], fail_silently=True
        #     )
        # except:
        #   try:
        #     po = PrintableOption.objects.filter(
        #       size_display=row[header_descriptor['variant']], parent=parent_po).first()
        #   except:
        #     po = None

        try:
          cart.date_closed_at = parse(row[header_descriptor['date_completed']]) # type: ignore
        except:
          cart.date_closed_at = datetime.datetime.now()

        cart.save()

        if header_descriptor['brurla']:
          brula = row[header_descriptor['brurla']] or ''
        else:
          brula = None

        if pd.name == "2TShirtsPlusOnesieSET_1stChristmas":

          dad_ig = ImageDesign.objects.create(
            stored_data={"name": "2TShirtsPlusOnesieSET_1stChristmas_Adult", "color": "", "attributes":
              {"Base Image": row[header_descriptor['designx']],
                "Pick a Name": row[header_descriptor['designd']]},
              "background": "", "all_designs": {
                  "Base Image": row[header_descriptor['designx']],
                  "Pick a Name": row[header_descriptor['designd']],
                }
              },
            image_creator_id=4664
          )

          cart.cartitem_set.create(
            product=pd,
            # Not required
            # printable_option_id=sizing_chart[row[header_descriptor['papa']]],
            qty=row[header_descriptor['qty']],
            design_1_source=dad_ig
          )

          mom_ig = ImageDesign.objects.create(
            stored_data={"name": "2TShirtsPlusOnesieSET_1stChristmas_Adult", "color": "", "attributes":
              {"Base Image": row[header_descriptor['designx']],
                "Pick a Name": row[header_descriptor['designm']]},
              "background": "", "all_designs": {
                  "Base Image": row[header_descriptor['designx']],
                  "Pick a Name": row[header_descriptor['designm']],
                }
              },
            image_creator_id=4664,
          )
          cart.cartitem_set.create(
            product=pd,
            # Not required
            # printable_option_id=sizing_chart[row[header_descriptor['mama']]],
            qty=row[header_descriptor['qty']],
            design_1_source=mom_ig
          )

          baby_ig = ImageDesign.objects.create(
            stored_data={"name": "2TShirtsPlusOnesieSET_1stChristmas_Adult", "color": "", "attributes":
              {"Base Image": row[header_descriptor['designx']],
                "Enter a Name": row[header_descriptor['designb']]},
              "background": "", "all_designs": {
                  "Base Image": row[header_descriptor['designb']],
                  "Enter a Name": row[header_descriptor['designm']],
                }
              },
            image_creator_id=4663
          )
          cart.cartitem_set.create(
            product=pd,
            # printable_option_id=sizing_baby[row[header_descriptor['baby']]],
            qty=row[header_descriptor['qty']],
            design_1_source=baby_ig,
          )

        elif pd.name == "GIFTBOX":
          cart.cartitem_set.create(
            product=pd,
            qty=row[header_descriptor['qty']],
          )

        else:
          cart.cartitem_set.create(
            product=pd,
            # Not required
            # product_variant=pv,
            # Not required
            # printable_option=po,
            qty=row[header_descriptor['qty']],
            front_pdf=row[header_descriptor['frurla']] or '',
            back_pdf=brula
          )

        # status = Status.objects.get(id=36)
        # if not cart.current_status.status.id == status.id:
        #   cart.current_status = CartStatus.objects.create(
        #     cart=cart, status=status)
        #   cart.save()

      if header_descriptor['brurla']:
        try:
          ci = CartItem.objects.get(front_pdf=row[header_descriptor['frurla']])
          ci.back_pdf = row[header_descriptor['brurla']]
          ci.save()
        except:
          pass
      
      invoice = None
      if len(new_carts) > 0:
        invoice = self.create_invoice()
      for c in old_carts:
        try:
          c['invoice']
        except:
          if invoice == None:
            invoice = self.create_invoice()
          c.invoice = invoice
          c.save()
      return new_carts, invoice

  def create_invoice(self):
    print('Create invoice')
    new_invoice = Invoice.objects.create()
    new_invoice.save()
    return new_invoice

  # Create order(s)
  def create_cart(self, row, header_descriptor, partner):
    print('Create cart')
    order_id = row[header_descriptor['order_number']]
    if order_id.startswith('#'):
      order_id = order_id[1:]
    print(order_id, row[header_descriptor['order_number']])
    cart, created = Cart.objects.get_or_create(
        # ???
        # store_id=self.store.id,
        # TODO
        # friendly_id=order_id, partner_id=partner)
        order_number=order_id,
        # TODO
        # partner_id=partner)
    )
    print(cart, created)
    cart.partner_id = partner
    cart.client_first_name = row[header_descriptor['client_full_name']].split(' ')[0]
    cart.client_last_name = ' '.join(row[header_descriptor['client_full_name']].split(' ')[1:])
    cart.client_name = row[header_descriptor['client_full_name']]
    cart.client_email = row[header_descriptor['client_email']]
    cart.client_address = row[header_descriptor['client_address']]
    cart.client_address_2 = row[header_descriptor['client_address_2']]
    cart.client_phone = row[header_descriptor['client_phone']]
    cart.client_city = row[header_descriptor['client_city']]
    cart.client_state = row[header_descriptor['client_state']]
    cart.client_zip = row[header_descriptor['client_zip']]
    cart.client_country = row[header_descriptor['client_country']]
    cart.save()

    # if created or hasattr(cart, 'cartstatus '):
    #   status, _ = Status.objects.get_or_create(
    #     name='Regist',
    #     color='grey',
    #   )
    #   status.save()

    #   cart_status, _ = CartStatus.objects.get_or_create(
    #     cart=cart,
    #     status=status,
    #   )
    #   print('here')
    #   cart_status.save()

      # cart.cartstatus = cart_status
      # cart.save()
    return cart, created

  def create_cart_item(self, ):
    # TODO Add cart_item.cost to cart.total_cost
    pass

  def add_item_to_cart(self, cart, cart_item):

    pass

@receiver(post_save, sender=FileUpload)
def my_handler2(sender, instance, **kwargs):
  upload = Upload(
    upload_method = 'MANUAL',
    file_upload = instance,
  )
  upload.save()

class Upload(models.Model):
  # belongs_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
  # status = models.ForeignKey(Status, on_delete=models.CASCADE)
  # ManyToMany
  # payment = models.ForeignKey(Invoice, on_delete=models.CASCADE)
  UPLOAD_METHOD_CHOICES = (
    ("MANUAL", "manual"),
    ("API", "api"),
  )
  upload_method = models.CharField(max_length=7, choices=UPLOAD_METHOD_CHOICES)
  date_uploaded = models.DateField(default=datetime.date.today)
  order = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
  file_upload = models.OneToOneField(FileUpload, on_delete=models.CASCADE, null=True, blank=True)
  api_upload = models.OneToOneField(ApiUpload, on_delete=models.CASCADE, null=True, blank=True)

@receiver(post_save, sender=Upload)
def my_handler(sender, instance, **kwargs):
  status, _ = Status.objects.get_or_create(
    name='Uploaded',
  )
  cart_status, _ = UploadStatus.objects.get_or_create(
    status=status,
    upload=instance,
  )

class UploadStatus(models.Model):
  status = models.ForeignKey(Status, on_delete=models.CASCADE)
  upload = models.OneToOneField(
    Upload,
    on_delete=models.CASCADE,
  )
