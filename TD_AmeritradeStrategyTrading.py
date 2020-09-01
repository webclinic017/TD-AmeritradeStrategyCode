from Client_ import TDClient
from TradeOrders import TDOrders
from config import client_id, password, accntNmber, userName
from datetime import datetime
from datetime import timedelta
from datetime import date
from Backtrader import Backtrader_main_
import json
import os
import pandas as pd
import numpy as np
import time
import pprint
#initialize new session with accnt info and caching false
TDSession = TDClient(account_number = accntNmber,
                     account_password = password,
                     redirect_uri = 'http://localhost/',
                     consumer_id = client_id,
                     #cache_state = True
                     )
TDSession.login()
print(TDSession.state['loggedin']) 
print(TDSession.authstate)
#Inputs
#Number of days desired for a moving average 0 is used as a value
    #e.g. for 10 days of data make the value below 11
Num_DayMAInputs = 50
symbol = TDSession.multiple_symbol_watchlist()
#OHLC Data
#Define parameters for Candles Data Open High Low Close (OHLC)
    #Accounts for weekend repetative data
for Symbol in symbol:
    hist_endDate = str(int(round(datetime.now().timestamp() * 1000)))
    hist_symbol = Symbol
    hist_period = 5
    hist_periodType = 'day'
    hist_frequencyType = 'minute'
    hist_frequency = 30
    hist_needExtendedHoursData = False
    Num_dayMA = Num_DayMAInputs
    for days in range (1,Num_dayMA,1):
        hist_startDate = str(int(round(((datetime.now() - timedelta(days=days)).timestamp()) * 1000)))
        HistDate = (int(round((datetime.now() - timedelta(days=days)).timestamp())))
        HistYear = datetime.fromtimestamp(HistDate).year
        HistMonth = datetime.fromtimestamp(HistDate).month
        HistDay = datetime.fromtimestamp(HistDate).day
        NumbDays = date(HistYear,HistMonth,HistDay).isoweekday()
        if NumbDays <= 5:
            if NumbDays <= Num_DayMAInputs:
                X_DayMA = TDSession.Historical_Endpoint(symbol=hist_symbol, 
                                                        period=hist_period,
                                                        period_type=hist_periodType,
                                                        frequency_type=hist_frequencyType,
                                                        start_date=hist_startDate,
                                                        end_date=hist_endDate,
                                                        frequency=hist_frequency,
                                                        extended_hours=hist_needExtendedHoursData
                                                       )
            else:
                False
    time.sleep(2)
#Call Simple moving average values for each symbol in watchlist
SimpleMovingAverage = TDSession._SMA_(symbol=symbol)
MACD_spanTwelve = TDSession.spanTwelveEMA(symbol=symbol)
MACD_spanTwntySix = TDSession.spanTwntySixEMA(symbol=symbol)
MACD = TDSession._MACD_(symbol=symbol)
MACD_Tickers = TDSession._MACD_Tickers(symbol=symbol)
SMA_toCSV = TDSession._SMA_toCSV(symbol=symbol, SimpleMovingAverage=SimpleMovingAverage)
EMA_toCSV = TDSession._EMA_toCSV(symbol=symbol,spantwelveEMA=MACD_spanTwelve, spanTwntySixEMA=MACD_spanTwntySix, _MACD_=MACD)
MACD_Signal = TDSession.MACD_Signal(symbol=symbol)
MACD_SignalToCSV = TDSession._MACD_SignaltoCSV(symbol=symbol,MACD_Signal=MACD_Signal)
SMABuyTickers = TDSession.SMABuyTickers(symbol=symbol)
print(SMABuyTickers)
MACD_buyTickers = TDSession.MACD_buyTickers(symbol=symbol)
print(MACD_buyTickers)
SMA_SellTickers = TDSession.SMA_SellTickers(symbol=symbol)
MACD_SellTickers = TDSession.MACD_SellTickers(symbol=symbol)
print(MACD_SellTickers)
#Account information to place orders
BuyingPower = TDSession.BuyingPower(accntNmber=accntNmber)
TD_Portfolio = TDSession.TDA_Portfolio(accntNmber=accntNmber, symbol=symbol)
print(TD_Portfolio)
Positions = TD_Portfolio.set_index('Ticker')
Positions = Positions.drop('MMDA1')
positions = list(Positions.index)
streamPrice = TDSession.readStream(positions=positions)
shares = TDSession.shareNum_buy(positions=positions)
#Simple Moving Average Logic
Buy = []
for position in SMABuyTickers:
    for SMABuyTickers in MACD_buyTickers:
        if not position in positions:
            if shares == 0:
                pass
            else:
                shares = shares
                print('Buy ' + position)
                PlaceMarketOrder = TDSession.place_order(accntNmber=accntNmber, shares=shares, ticker=position)
                #BuyOrderSummary = TDSession.buyorderSummary(shares=shares, ticker=position)
        else:
            print('You already own' + ' ' + position)
Sell = []
for position in positions:
    if position in MACD_SellTickers:
        ticker = TD_Portfolio.set_index('Ticker')
        Positions = ticker.to_dict(orient='dict')
        shares = Positions['Quantity'][position]
        print('Sell' + ' ' + position)
        SellMarketOrder = TDSession.sellPositions(accntNmber=accntNmber, shares=shares, ticker=position)
        print(position + 'Sold')
        #SellOrderSummary = TDSession.sellorderSummary(shares=shares, ticker=position)
    else:
        pass
'''
#Develop a strategy backtrader using the documentation at this website https://www.backtrader.com/
    #Backtrader Simple moving average example https://towardsdatascience.com/trading-strategy-back-testing-with-backtrader-6c173f29e37f
        #https://community.backtrader.com/topic/122/bband-strategy
#Run Backtrader
RunBacktrader = Backtrader_main_._Backtrader_()
'''
