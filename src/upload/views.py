from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from django.core.mail import send_mail

from .models import UploadedFile
from payment.models import Invoice
from order.models import Cart, CartItem, CartStatus
from catalog.models import Product

import csv
import datetime

# Create your views here.

class UploadIndexView(ListView):
  model = UploadedFile
  template_name = 'upload/index.html'
  context_object_name = 'files'


  def process_csv_header(self, csv_file):
    reader = csv.reader(csv_file, delimiter=';')
    first_row = next(reader)

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

    

    try:
      product = first_row.index('Product Type')
    except:
      product = first_row.index('SKU')

    try:
      designx = first_row.index('Main design file name (.png)')
      designd = first_row.index('Dad title title image file (.png)')
      designm = first_row.index('Mom title image file (.png)')
      designb = first_row.index("Baby's name (Text)")
      papa = first_row.index("Dad Tshirt Size")
      mama = first_row.index("Mom Tshirt Size")
      baby = first_row.index("Baby's OneSie Size")
    except:
      pass

    
    try:
      variant = first_row.index('size')
    except:
      try:
        variant = first_row.index('Size')
      except:
        variant = None

    full_name = first_row.index('Shipping Fullname')
    phone = first_row.index('Phone')

    try:
      date_completed = first_row.index('order date')
    except:
      date_completed = ""

    
    email = first_row.index('Email')
    address = first_row.index('Address1')
    address_2 = first_row.index('Address2')
    city = first_row.index('City')
    state = first_row.index('Province')
    zip = first_row.index('Zip')
    country = first_row.index('Country Code')

    try:
        qty = first_row.index('UnFulfill Quantity')
    except:
        qty = first_row.index('Qty')
    frurla = first_row.index('Printer Design Url Front')

    try:
        brurla = first_row.index('Printer Design Url Back')
    except:
        brurla = None

    header_descriptor = {
      'order_number': order_number,
      'product': product,
      'designx': designx,
      'designd': designd,
      'designm': designm,
      'designb': designb,
      'papa': papa,
      'mama': mama,
      'baby': baby,
      'variant': variant,
      'full_name': full_name,
      'phone': phone,
      'date_completed': date_completed,
      'email': email,
      'address': address,
      'address_2': address_2,
      'city': city,
      'state': state,
      'zip': zip,
      'country': country,
      'qty': qty,
      'frurla': frurla,
      'brurla': brurla,
    }

    return header_descriptor

  def process_csv_body(self, csv_file, header_descriptor, partner, cart):
    new_carts = []
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

    reader = csv.reader(csv_file, delimiter=';')
    next(reader)

    for row in reader:
      order_id = ''.join(filter(str.isdigit, row[int(header_descriptor['order_number'])]))
      if order_id.startswith('#'):
        order_id = order_id[1:]
      cart, created = Cart.objects.get_or_create(
        # ???
        # store_id=self.store.id,
        friendly_id=order_id, partner_id=partner)
      cart.partner_id = partner
      cart.client_first_name = row[header_descriptor['full_name']].split(' ')[0]
      cart.client_last_name = ' '.join(row[header_descriptor['full_name']].split(' ')[1:])
      cart.client_name = row[header_descriptor['full_name']]
      cart.client_email = row[header_descriptor['email']]
      cart.client_address = row[header_descriptor['address']]
      cart.client_address_2 = row[header_descriptor['address_2']]
      cart.client_phone = row[header_descriptor['phone']]
      cart.client_city = row[header_descriptor['city']]
      cart.client_state = row[header_descriptor['state']]
      cart.client_zip = row[header_descriptor['zip']]
      cart.client_country = row[header_descriptor['country']]
      cart.save()

      if created:
        # Create invoice for cart
        InvoiceCart.objects.create(cart=cart, invoice=new_invoice)
        # Assign cart status
        cart.current_status = CartStatus.objects.create(
          cart=cart, status_id=36)
        cart.save()
        new_carts.append(cart)
      else:
        if cart in new_carts:
          pass
        else:
          messages.add_message(
            self.request, messages.INFO, 'Cart #%s' % cart.friendly_id)

      # Will run twices if created
      if cart in new_carts or created:
        cart.current_status = CartStatus.objects.create(
          cart=cart, status_id=36)
        pd, created = Product.objects.get_or_create(
          store_id=10, name=row[header_descriptor['product']])
        if created:
          messages.add_message(
            self.request, messages.INFO, 'New Product #%s' % pd.id)
        if created:
          send_mail(
            subject='New Gossby Product',
            message='New Gossby Product - %s' % pd.id,
            from_email='info@mayamedia.io', recipient_list=['info@mayamedia.io'], fail_silently=True
          )
        if header_descriptor['variant']:
          pv, created = ProductVariant.objects.get_or_create(
            product=pd, name=row[header_descriptor['variant']])
          if created:
            send_mail(
              subject='New Gossby Product - Variant',
              message='New Gossby Product - %s' % pv.id,
              from_email='info@mayamedia.io', recipient_list=['info@mayamedia.io'], fail_silently=True
            )

        parent_po, created = Printable.objects.get_or_create(
          title='_'.join(row[header_descriptor['product']].split('_')[:-1]))

        if created:
          send_mail(
            subject='New Gossby Printable',
            message='New Gossby Product - %s' % parent_po.id,
            from_email='info@mayamedia.io', recipient_list=['info@mayamedia.io'], fail_silently=True
          )

        try:
          po, created = PrintableOption.objects.get_or_create(
            size_display=row[header_descriptor['variant']], parent=parent_po)
          if created:
            send_mail(
              subject='New Gossby Product - PrintableOption',
              message='New Gossby Product - %s' % po.id,
              from_email='info@mayamedia.io', recipient_list=['info@mayamedia.io'], fail_silently=True
            )
        except:
          try:
            po = PrintableOption.objects.filter(
              size_display=row[header_descriptor['variant']], parent=parent_po).first()
          except:
            po = None

        try:
          # ???
          cart.date_closed_at = parse(row[header_descriptor['date_completed']])
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
            printable_option_id=sizing_chart[row[header_descriptor['papa']]],
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
            printable_option_id=sizing_chart[row[header_descriptor['mama']]],
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
            printable_option_id=sizing_baby[row[header_descriptor['baby']]],
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
            product_variant=pv,
            printable_option=po,
            qty=row[header_descriptor['qty']],
            front_pdf=row[header_descriptor['frurla']] or '',
            back_pdf=brula
          )

        if not cart.current_status.status_id == 36:
          cart.current_status = CartStatus.objects.create(
            cart=cart, status_id=36)
          cart.save()

      if header_descriptor['brurla']:
        ci = CartItem.objects.get(front_pdf=row[header_descriptor['frurla']])
        ci.back_pdf = row[header_descriptor['brurla']]
        ci.save()

  def create_invoice():
    new_invoice = Invoice.objects.create()
    return new_invoice

  # Create order(s)
  def create_cart():
    new_cart = Cart.objects.create()
    return new_cart

  def get_context_data(self, *args, **kwargs):
    ctx = super().get_context_data(*args, **kwargs)
    ctx['partners'] = User.objects.filter(
        is_superuser=False, is_staff=False)
    return ctx

  def post(self, *args, **kwargs):
    print(self.request.POST)

    context = self.get_context_data(**kwargs)

    partner = self.request.POST.get('partner')
    try:
      csv_file = self.request.FILES["file"].file.read().decode(
          'utf-8-sig').splitlines()
    except MultiValueDictKeyError:
      print('TODO')
      return render(self.request, 'upload/index.html')

    new_invoice = self.create_invoice() 
    cart = self.create_cart() 
    header_descriptor = self.process_csv_header(csv_file)
    self.process_csv_body(csv_file, header_descriptor, partner, cart)
    return render(self.request, 'upload/index.html', {'new_invoice_id': new_invoice.id}, )
