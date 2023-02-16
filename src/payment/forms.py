from django import forms

METHODS = (
  ("STRIPE", "Stripe"),
  ("PAYPAL", "PayPal"),
)
  
class AddPaymentForm(forms.Form):
  # TODO Make it dropdown
  name = forms.ChoiceField(
    required=False,
    choices=METHODS,
    widget=forms.Select(attrs={'class': 'dropdown'}),
  )
  token = forms.CharField(max_length=20)

