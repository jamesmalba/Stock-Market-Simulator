from django.shortcuts import render, redirect
from .models import Stock, Portfolio
from .forms import StockActionForm
import yfinance as yf
import pandas as pd

def portfolio_home(request):
    return update_stocks(request)

def stock_transaction(request):
    # check if portfolio exists             
    portfolio = Portfolio.objects.all().first()
    if not portfolio:
        portfolio = Portfolio(balance = 10000, age = 0)
        portfolio.save()

    if 'buy_stock' in request.POST:
        form = StockActionForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol']
            amount = form.cleaned_data['amount']
            price = form.cleaned_data['price']

            stock = Stock.objects.filter(symbol = symbol).first()
            if stock == None:
                stock_data = yf.Ticker(symbol)
                stockinfo = stock_data.info['sharesOutstanding']

                new_stock = Stock(symbol = symbol, name = stock_data.info['shortName'], price = stock_data.info['previousClose'], order_amount = amount,
                            market_cap = float(str(stock_data.info['marketCap'])[:3])/10, cost = (amount * price), amount_owned = 0, limit_price = price)
                new_stock.save()
                pass
            portfolio_check = Portfolio.objects.all().first()
            
            if stock and stock.price <= price and (stock.price * amount) <= portfolio_check.balance:
                portfolio_check.balance -= (stock.price * amount)
                stock.cost = stock.price * amount
                portfolio_check.save()

                # update amount owned of stock
                stock.amount_owned += amount
                stock.order_amount -= amount
                stock.save()
                return update_stocks(request)
    else: 
        form = StockActionForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol']
            amount = form.cleaned_data['amount']
            price = form.cleaned_data['price']

            stock = Stock.objects.filter(symbol = symbol).first()
            if stock == None:
                print("stock does not exist")
                return update_stocks(request) 

            portfolio_check = Portfolio.objects.all().first()
            if price <= stock.price:
                portfolio_check.balance += (stock.price * amount)
                portfolio_check.save()

                # update amount owned of stock
                stock.amount_owned -= amount
                stock.save()
                return update_stocks(request)

    return update_stocks(request)

def update_stocks(request):
    stock_check = Stock.objects.filter(amount_owned = 0)
    if stock_check != None: 
        for stock in stock_check:
            portfolio = Portfolio.objects.all().first()
            while stock.price <= stock.limit_price and stock.order_amount != 0:
                # update amount owned of stock
                stock.amount_owned += 1
                stock.order_amount -= 1
                stock.save()

                # update portfolio balance
                portfolio.balance -= 1 * stock.price
                portfolio.save()

                
    stocks = Stock.objects.exclude(amount_owned = 0)
    for i in stocks:
        print(i)
    orders = Stock.objects.filter(amount_owned = 0).first()
    portfolio = Portfolio.objects.exclude(balance = 0).first()
    context = {'stocks': stocks, 'portfolio': portfolio, 'active_orders': orders}
    return render(request, 'home.html', context)