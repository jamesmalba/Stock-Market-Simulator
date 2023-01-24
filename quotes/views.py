from django.shortcuts import render, redirect
from .models import Stock, Portfolio
from .forms import StockActionForm
import pandas as pd
import yfinance as yf
from django.contrib.auth import authenticate, login

def portfolio_home(request):
    return update_stocks(request)

def stock_transaction(request):
    # check if portfolio exists
    try:                 
        portfolio = Portfolio.objects.all()
    except Portfolio.DoesNotExist:
        portfolio = Portfolio(balance = 10000, age = 0)
        portfolio.save()

    if 'buy_stock' in request.POST:
        form = StockActionForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol']
            amount = form.cleaned_data['amount']
            price = form.cleaned_data['price']

            try:                 
                stock = Stock.objects.get(symbol = symbol)
            except Stock.DoesNotExist:
                stock_data = yf.Ticker(symbol)
                stock_df = stock_data.history(period = '1d')            
                stock = Stock(symbol = stock_df.ticker, name = stock_df.info['longName'], price = stock_df.Close[-1], 
                            market_cap = stock_df.MarketCap[-1], change = stock_df.Change[-1], cost = amount * price, amount_owned = 0, limit_price = price)
                stock.save()
                pass
            portfolio = Portfolio.objects.get(user = request.user)
            if stock.price <= price and stock.cost <= portfolio.balance:
                portfolio.balance -= stock.cost
                portfolio.save()

                # update amount owned of stock
                stock.amount_owned += amount
                stock.save()
                return redirect('')
    else: 
        form = StockActionForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol']
            amount = form.cleaned_data['amount']
            price = form.cleaned_data['price']

            try:                 
                stock = Stock.objects.get(symbol = symbol)
            except Stock.DoesNotExist:
                print("stock does not exist")
                return update_stocks(request) 

            portfolio = Portfolio.objects.get(user = request.user)
            if stock.price <= price:
                portfolio.balance += (price * amount)
                portfolio.save()

                # update amount owned of stock
                stock.amount_owned -= amount
                stock.save()
                return redirect('')

    update_stocks(request)

def update_stocks(request):
    stock_check = Stock.objects.filter(amount_owned = 0)
    if stock_check != None: 
        for stock in stock_check:
            portfolio = Portfolio.objects.get(user = request.user)
            if stock.limit_price <= stock.price and stock.cost <= portfolio.balance:
                # update portfolio balance
                portfolio.balance -= stock.cost
                portfolio.save()

                # update amount owned of stock
                stock.amount_owned += (stock.cost / stock.limit_price)
                stock.save()
    stocks = Stock.objects.exclude(amount_owned = 0)
    orders = Stock.objects.filter(amount_owned = 0)
    portfolio = Portfolio.objects.exclude(balance = 0)
    context = {'stocks': stocks, 'portfolio': portfolio, 'active_orders': orders}
    return render(request, 'home.html', context)