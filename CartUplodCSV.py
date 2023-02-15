class CartUploadCSV(CurrentStore, TemplateView):
    template_name = "dashboard/orders/upload.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['partners'] = User.objects.filter(
            is_superuser=False, is_staff=False)
        return ctx

    def post(self, *args, **kwargs):
        partner = self.request.POST.get('partner')
        csv_file = self.request.FILES["csv_file"].file.read().decode(
            'utf-8-sig').splitlines()
        new_invoice = Invoice.objects.create()
        reader = csv.reader(csv_file, delimiter=';')
        row1 = next(reader)
        try:
            order_number = row1.index('Code')
        except:
            reader = csv.reader(csv_file, delimiter=',')
            row1 = next(reader)
            order_number = row1.index('Code')
        try:
            product = row1.index('Product Type')
        except:
            product = row1.index('SKU')
        try:
            designx = row1.index('Main design file name (.png)')
            designd = row1.index('Dad title title image file (.png)')
            designm = row1.index('Mom title image file (.png)')
            designb = row1.index("Baby's name (Text)")
            papa = row1.index("Dad Tshirt Size")
            mama = row1.index("Mom Tshirt Size")
            baby = row1.index("Baby's OneSie Size")
        except:
            pass
        try:
            variant = row1.index('size')
        except:
            try:
                variant = row1.index('Size')
            except:
                variant = None

        full_name = row1.index('Shipping Fullname')
        phone = row1.index('Phone')
        try:
            date_completed = row1.index('order date')
        except:
            date_completed = ""

        email = row1.index('Email')
        address = row1.index('Address1')
        address_2 = row1.index('Address2')
        city = row1.index('City')
        state = row1.index('Province')
        zip = row1.index('Zip')
        country = row1.index('Country Code')
        try:
            qty = row1.index('UnFulfill Quantity')
        except:
            qty = row1.index('Qty')
        frurla = row1.index('Printer Design Url Front')
        try:
            brurla = row1.index('Printer Design Url Back')
        except:
            brurla = None
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
        for row in reader:
            order_id = ''.join(filter(str.isdigit, row[int(order_number)]))
            if order_id.startswith('#'):
                order_id = order_id[1:]
            cart, created = Cart.objects.get_or_create(
                store_id=self.store.id, friendly_id=order_id, partner_id=partner)
            cart.partner_id = partner
            cart.client_first_name = row[full_name].split(' ')[0]
            cart.client_last_name = ' '.join(row[full_name].split(' ')[1:])
            cart.client_name = row[full_name]
            cart.client_email = row[email]
            cart.client_address = row[address]
            cart.client_address_2 = row[address_2]
            cart.client_phone = row[phone]
            cart.client_city = row[city]
            cart.client_state = row[state]
            cart.client_zip = row[zip]
            cart.client_country = row[country]
            cart.save()
            if created:
                InvoiceCart.objects.create(cart=cart, invoice=new_invoice)
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
            if cart in new_carts or created:
                cart.current_status = CartStatus.objects.create(
                    cart=cart, status_id=36)
                pd, created = Product.objects.get_or_create(
                    store_id=10, name=row[product])
                if created:
                    messages.add_message(
                        self.request, messages.INFO, 'New Product #%s' % pd.id)
                if created:
                    send_mail(
                        subject='New Gossby Product',
                        message='New Gossby Product - %s' % pd.id,
                        from_email='info@mayamedia.io', recipient_list=['info@mayamedia.io'], fail_silently=True
                    )
                if variant:
                    pv, created = ProductVariant.objects.get_or_create(
                        product=pd, name=row[variant])
                    if created:
                        send_mail(
                            subject='New Gossby Product - Variant',
                            message='New Gossby Product - %s' % pv.id,
                            from_email='info@mayamedia.io', recipient_list=['info@mayamedia.io'], fail_silently=True
                        )

                parent_po, created = Printable.objects.get_or_create(
                    title='_'.join(row[product].split('_')[:-1]))
                if created:
                    send_mail(
                        subject='New Gossby Printable',
                        message='New Gossby Product - %s' % parent_po.id,
                        from_email='info@mayamedia.io', recipient_list=['info@mayamedia.io'], fail_silently=True
                    )
                try:
                    po, created = PrintableOption.objects.get_or_create(
                        size_display=row[variant], parent=parent_po)
                    if created:
                        send_mail(
                            subject='New Gossby Product - PrintableOption',
                            message='New Gossby Product - %s' % po.id,
                            from_email='info@mayamedia.io', recipient_list=['info@mayamedia.io'], fail_silently=True
                        )

                except:
                    try:
                        po = PrintableOption.objects.filter(
                            size_display=row[variant], parent=parent_po).first()
                    except:
                        po = None

                try:
                    cart.date_closed_at = parse(row[date_completed])
                except:
                    cart.date_closed_at = datetime.datetime.now()
                cart.save()
                if brurla:
                    brula = row[brurla] or ''
                else:
                    brula = None
                if pd.name == "2TShirtsPlusOnesieSET_1stChristmas":
                    dad_ig = ImageDesign.objects.create(
                        stored_data={"name": "2TShirtsPlusOnesieSET_1stChristmas_Adult", "color": "", "attributes":
                                     {"Base Image": row[designx],
                                         "Pick a Name": row[designd]},
                                     "background": "", "all_designs": {"Base Image": row[designx], "Pick a Name": row[designd]}
                                     },
                        image_creator_id=4664
                    )
                    cart.cartitem_set.create(
                        product=pd,
                        printable_option_id=sizing_chart[row[papa]],
                        qty=row[qty],
                        design_1_source=dad_ig
                    )
                    mom_ig = ImageDesign.objects.create(
                        stored_data={"name": "2TShirtsPlusOnesieSET_1stChristmas_Adult", "color": "", "attributes":
                                     {"Base Image": row[designx],
                                         "Pick a Name": row[designm]},
                                     "background": "", "all_designs": {"Base Image": row[designx], "Pick a Name": row[designm]}
                                     },
                        image_creator_id=4664,

                    )
                    cart.cartitem_set.create(
                        product=pd,
                        printable_option_id=sizing_chart[row[mama]],
                        qty=row[qty],
                        design_1_source=mom_ig
                    )
                    baby_ig = ImageDesign.objects.create(
                        stored_data={"name": "2TShirtsPlusOnesieSET_1stChristmas_Adult", "color": "", "attributes":
                                     {"Base Image": row[designx],
                                         "Enter a Name": row[designb]},
                                     "background": "", "all_designs": {"Base Image": row[designb], "Enter a Name": row[designm]}
                                     },
                        image_creator_id=4663
                    )
                    cart.cartitem_set.create(
                        product=pd,
                        printable_option_id=sizing_baby[row[baby]],
                        qty=row[qty],
                        design_1_source=baby_ig
                    )
                elif pd.name == "GIFTBOX":
                    cart.cartitem_set.create(
                        product=pd,
                        qty=row[qty]
                    )
                else:
                    cart.cartitem_set.create(
                        product=pd,
                        product_variant=pv,
                        printable_option=po,
                        qty=row[qty],
                        front_pdf=row[frurla] or '',
                        back_pdf=brula
                    )
                if not cart.current_status.status_id == 36:
                    cart.current_status = CartStatus.objects.create(
                        cart=cart, status_id=36)
                    cart.save()
            if brurla:
                ci = CartItem.objects.get(front_pdf=row[frurla])
                ci.back_pdf = row[brurla]
                ci.save()

        context = self.get_context_data(**kwargs)
        return HttpResponseRedirect(reverse('invoice-detail', kwargs={'pk': new_invoice.id}))
