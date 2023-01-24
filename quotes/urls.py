from django.urls import path
from .views import stock_transaction, portfolio_home
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# URLConf
urlpatterns = [
    path('transaction/', stock_transaction, name = 'stock_transaction'),
    path('', portfolio_home, name = "portfolio_home"),
]