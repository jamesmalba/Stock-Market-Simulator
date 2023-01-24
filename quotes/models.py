from django.db import models

class Stock(models.Model):
    symbol = models.CharField(max_length = 10)
    name = models.CharField(max_length = 100)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    market_cap = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
    cost = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
    limit_price = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
    change = models.DecimalField(max_digits = 10, decimal_places = 2)
    amount_owned = models.IntegerField(default = 0)

class Portfolio(models.Model):
    balance = models.DecimalField(max_digits = 10, decimal_places = 2, default = 10000.00)
    age = models.IntegerField(default = 0)
