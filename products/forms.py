from django import forms
from decimal import Decimal, InvalidOperation

CONTACT_METHOD_CHOICES = [
    ('email', 'ایمیل'),
    ('telegram', 'تلگرام'),
]

class PriceAlertForm(forms.Form):
    product_slug = forms.CharField(widget=forms.HiddenInput())
    contact = forms.EmailField(label='ایمیل', max_length=254)
    contact_method = forms.ChoiceField(choices=CONTACT_METHOD_CHOICES, initial='email')
    target_price = forms.DecimalField(label='قیمت هدف (ریال)', min_value=Decimal('1.00'), decimal_places=2)

class CalculatorForm(forms.Form):
    product_slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    product = forms.ChoiceField(choices=[], required=False, label='محصول')
    price = forms.DecimalField(label='قیمت واحد (ریال)', max_digits=20, decimal_places=2, required=False)
    quantity = forms.DecimalField(label='تعداد / وزن', required=False, decimal_places=3)
    budget = forms.DecimalField(label='بودجه (ریال)', required=False, max_digits=20, decimal_places=2)

    def clean(self):
        cleaned = super().clean()
        q = cleaned.get('quantity')
        b = cleaned.get('budget')
        if not q and not b:
            raise forms.ValidationError("یا مقدار (تعداد/وزن) وارد کنید یا بودجه را.")
        return cleaned