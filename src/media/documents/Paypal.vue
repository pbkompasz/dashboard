<div id="paypal-button-container"></div>
<form method="POST" action="" id="payment-form" @submit="paymentPrevent">
  {% csrf_token %}
  {% if request.user.is_authenticated %}
  <input type="hidden" name="test" value="test" />
  {% endif %}
  <input type="hidden" v-model="first_name" name="firstname" />
  <input type="hidden" v-model="last_name" name="laststname" />
  <input type="hidden" v-model="email" name="email" />
  <input type="hidden" v-model="phone" name="phone" />
  <input type="hidden" name="bump|printoption" v-model="bumprintoption" />
  <input type="hidden" v-model="address" name="address" />
  <input type="hidden" v-model="address_2" name="address_2" />
  <input type="hidden" v-model="bumpcustom" id="bumpcustom" name='bump|customization' />
  <input type="hidden" v-model="city" name="city" />
  <input type="hidden" v-model="state" name="state" />
  <input type="hidden" v-model="country" name="country" />
  <input type="hidden" v-model="zip" name="zip" />
  <input type="hidden" v-if="shipping" v-model="shipping.id" name="shipping" />
  <input type="hidden" v-model="bump" name="bump" />
  {% if request.GET.set_test %}
  <input type="hidden" name="set_test" value="true" />
  {% endif %}

  <input type="hidden" id="paypal" name="paypal" />
  <input type="hidden" id="cpid" name="cpid" value="{{ cpid.id }}" />
  <input type="hidden" name="pvbump" :value="pvbump" />
  <input type="hidden" name="design_1" value="{{ checkout.get_first_design_uuid }}" />

</form>
<script>
let pj = paypal_sdk.Buttons({
  style: {
    layout: 'horizontal',
    height: 45,
  },
  createOrder: function (data, actions) {

    return actions.order.create({
      purchase_units: [{
        amount: {
          "currency_code": "{{ currency.short_hand }}",
          "value": _this.cart.total.toFixed(2),
          "breakdown": {
            "item_total": {
              "currency_code": "{{ currency.short_hand }}",
              "value": _this.getBumpPrice(),
            },
            "shipping": {
              "currency_code": "{{ currency.short_hand }}",
              "value": _this.getNetShipping(),
            },
            "discount": {
              "currency_code": "{{ currency.short_hand }}",
              "value": _this.cart.discounts.total.toFixed(2)
            }
          },

        }
      }]
    });
  },
  onApprove: function (data, actions) {
    let loader = _this.$loading.show({ loader: 'dots' })
    return fetch('/api-cart/paypal/', {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({
        orderID: data.orderID,
        checkoutID: '{{ checkout.id }}',
        shippingID: shippingID,
                                {% if request.user.is_authenticated %}
                                    test: 'true',
      {% endif %}
})
                        }).then(function (res) {

  if (!res.ok) {
    throw Error(res.statusText);
    _this.$loading.show({ loader: 'dots' })
  }

  document.getElementById('paypal').value = res.status;

  document.getElementById('payment-form').submit();
}).then(function (details) {
  if (details.error === 'INSTRUMENT_DECLINED') {
    loader.hide();
    return actions.restart();
  }
}).catch(function (err) {
  loader.hide();
});
                    }
                });
pj.render('#paypal-button-container');
</script>
