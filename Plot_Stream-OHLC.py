import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import datestr2num
import matplotlib.mlab as mlab
import pandas as pd
import numpy as np
from datetime import datetime
import csv
from matplotlib.animation import FuncAnimation
import matplotlib
import os
from config import client_id, password, accntNmber, userName
import requests
import time
from Client_ import TDClient
import mpl_finance as mpf


TDPlot = TDClient(account_number = accntNmber,
                  account_password = password,
                  redirect_uri = 'http://localhost/',
                  consumer_id = client_id,
                  )
symbol = TDPlot.multiple_symbol_watchlist()
Date = time.strftime('%Y-%m-%d', time.localtime()) 
os.chdir('C:\SourceCode\TD-AmeritradeAPI\Data' + '\\' + Date + '\\' + 'OHLC')
for ticker in symbol:
    dataFile = (ticker + '_' + 'OHLC' + '_' + Date + '.csv')
    data = pd.read_csv(dataFile)
    quotes = zip(datestr2num(data['Date']),data['Open'],data['High'],data['Low'],data['Close'])
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(12,6))
    mpf.candlestick_ohlc(ax, quotes, width=0.5, colorup='g', colordown='r')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price($)')
    ax.set_title(ticker +' OHLC & Simple Moving Average')
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    fig.autofmt_xdate()
    plt.show()












