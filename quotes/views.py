from django.shortcuts import render, redirect
from .models import Stock, Trade, Portfolio, User
import pandas as pd
import yfinance as yf
from django.contrib.auth import authenticate, login
# brain

def stock_list(request):
    stock_symbol = 'AAPL'
    stock_data = yf.Ticker(stock_symbol)
    stock_df = stock_data.history(period='1d')
    return render(request, 'stock_list.html', {'stock_df': stock_df})

def stock_detail(request, pk):
    stock = Stock.objects.get(pk = pk)
    trades = Trade.objects.filter(stock = stock)
    return render(request, 'stock_detail.html', {'stock': stock, 'trades': trades})

def stock_update(request, pk):
    stock = Stock.objects.get(pk = pk)
    stock_data = yf.Ticker(stock.symbol)
    stock.price = stock_data.info['regularMarketPrice']
    stock.save()
    return redirect('stock_detail', pk = stock.pk)

def make_trade(request):
    if request.method == 'POST':
        if not request.user.portfolio_set.exists():
            portfolio = Portfolio.objects.create(user=request.user)
        
        try:
            stock = Stock.objects.get(symbol=request.POST['stock_symbol'])
        except Stock.DoesNotExist:
            return redirect('stock_list')
        
        trade = Trade.objects.create(stock=stock, quantity=request.POST['quantity'], price=request.POST['price'], portfolio=portfolio)
        return redirect('trade_confirmation', pk=trade.pk)
    else:
        return render(request, 'trade.html')

def trade_confirmation(request, pk):
    trade = Trade.objects.get(pk=pk)
    return render(request, 'trade_confirmation.html', {'trade': trade})

def portfolio_home(request):
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = 'password'
        user = User.objects.create_user(username = username, password = password)
        user.account_balance = 10000
        user.save()
      
        user = authenticate(request, username = username, password = password)
        login(request, user)
   
    return render(request, 'home.html', {'user': request.user})