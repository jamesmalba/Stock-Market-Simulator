from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Stock(models.Model):
    symbol = models.CharField(max_length = 10)
    name = models.CharField(max_length = 100)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    quantity = models.IntegerField()

class Trade(models.Model):
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add = True)

class User(AbstractUser):
    balance = models.DecimalField(max_digits = 10, decimal_places = 2, default = 10000)
    groups = models.ManyToManyField(Group, blank=True, related_name='custom_user')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='custom_user')

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE)     
    quantity = models.IntegerField(default = 0)
