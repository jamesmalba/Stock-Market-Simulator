from django.urls import path
from .views import stock_list, stock_detail, stock_update, portfolio_home, make_trade
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# URLConf
urlpatterns = [
    path('stocks/', stock_list, name = "stock_list"),
    path('<int:pk>/', stock_detail, name = 'stock_detail'),
    path('<int:pk>/update/', stock_update, name='stock_update'),
    path('', portfolio_home, name = "portfolio_home"),
    path('trade/', make_trade, name = "make_trade")
]

urlpatterns += staticfiles_urlpatterns()