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
Num_DayMAInputs = 70
symbol = TDSession.multiple_symbol_watchlist()
#OHLC Data
#Define parameters for Candles Data Open High Low Close (OHLC)
    #Accounts for weekend repetative data 
for Symbol in symbol:
    hist_endDate = str(int(round(datetime.now().timestamp() * 1000)))
    hist_symbol = Symbol
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
            X_DayMA = TDSession.Historical_Endpoint(symbol=hist_symbol, 
                                                    period_type=hist_periodType,
                                                    frequency_type=hist_frequencyType,
                                                    start_date=hist_startDate,
                                                    end_date=hist_endDate,
                                                    frequency=hist_frequency,
                                                    extended_hours=hist_needExtendedHoursData
                                                   )
        else:
            False
#Call Simple moving average valuse for each symbol in watchlist
SimpleMovingAverage = TDSession._SMA_(symbol=symbol)
TDSession._SMA_toCSV(symbol=symbol,SimpleMovingAverage=SimpleMovingAverage)
positions = TDSession.accounts(accntNmber=accntNmber)
fiftyDaySMA = TDSession.fiftyDaySMA(symbol=symbol)
print(fiftyDaySMA)
#PLACING ORDERS WORKS MAKE SURE TURNED OFF!
#PlaceMarketOrder = TDSession.place_order(accntNmber=accntNmber)
'''
#Develop a strategy backtrader using the documentation at this website https://www.backtrader.com/
    #Backtrader Simple moving average example https://towardsdatascience.com/trading-strategy-back-testing-with-backtrader-6c173f29e37f
        #https://community.backtrader.com/topic/122/bband-strategy
#Run Backtrader
RunBacktrader = Backtrader_main_._Backtrader_()
'''
