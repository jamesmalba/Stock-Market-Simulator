from django import forms

class StockActionForm(forms.Form):
    symbol = forms.CharField(max_length = 6)
    amount = forms.IntegerField()
    price = forms.DecimalField(max_digits = 10, decimal_places = 2)