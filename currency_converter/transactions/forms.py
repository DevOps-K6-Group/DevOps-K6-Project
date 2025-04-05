from django import forms
from .models import Transaction

class ExchangeCurrencyForm(forms.Form):
    amount_usd = forms.DecimalField(max_digits=10, decimal_places=2)

class TransferMoneyForm(forms.Form):
    receiver_username = forms.CharField(max_length=150)
    amount_usd = forms.DecimalField(max_digits=10, decimal_places=2)