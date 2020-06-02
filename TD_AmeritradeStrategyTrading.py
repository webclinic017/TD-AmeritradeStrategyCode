from Client_ import TDClient
from config import client_id, password, accntNmber, userName
from datetime import datetime
from datetime import timedelta
from Backtrader import Backtrader_main_
import json
import os
import pandas as pd
import numpy as np
import time
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
Num_DayMAInputs = 21
symbol = TDSession.multiple_symbol_watchlist()
'''
#OHLC Data
#Define parameters for Candles Data Open High Low Close (OHLC)
for Symbol in symbol:
    hist_endDate = str(int(round(datetime.now().timestamp() * 1000)))
    hist_symbol = Symbol
    hist_periodType = 'day'
    hist_frequencyType = 'minute'
    hist_frequency = 1
    hist_needExtendedHoursData = True
    Num_dayMA = Num_DayMAInputs
    for days in range (1,Num_dayMA,1):
        hist_startDate = str(int(round(((datetime.now() - timedelta(days=days)).timestamp()) * 1000)))
        X_DayMA = TDSession.Historical_Endpoint(
                                                symbol=hist_symbol, 
                                                period_type=hist_periodType,
                                                frequency_type=hist_frequencyType,
                                                start_date=hist_startDate,
                                                end_date=hist_endDate,
                                                frequency=hist_frequency,
                                                extended_hours=hist_needExtendedHoursData
                                               )
def _SMA_():
    Date = time.strftime('%Y-%m-%d', time.localtime()) 
    os.chdir('C:\SourceCode\TD-AmeritradeAPI\Data' + '\\' + Date + '\\' + 'OHLC')
    dfSMA = {}
    for Ticker in symbol:
        dfSMA[Ticker] = pd.read_csv(Ticker + '_' + 'OHLC' + '_' + Date + '.csv')
    print(dfSMA)
_SMA_()
'''
#Start Straming Session
TDStreamer = TDSession.create_streaming_session()
TDStreamer.CSV_APPEND_MODE = True
TDStreamer.level_one_quote(symbols=symbol, fields=['0','1','2','3'])
TDStreamer.stream()
'''
#Develop a strategy backtrader using the documentation at this website https://www.backtrader.com/
    #Backtrader Simple moving average example https://towardsdatascience.com/trading-strategy-back-testing-with-backtrader-6c173f29e37f
        #https://community.backtrader.com/topic/122/bband-strategy
#Run Backtrader
RunBacktrader = Backtrader_main_._Backtrader_()
'''
