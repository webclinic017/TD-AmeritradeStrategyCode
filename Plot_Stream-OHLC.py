import matplotlib.pyplot as plt
import pandas as pd
import csv
from matplotlib.animation import FuncAnimation
import os
from config import client_id, password, accntNmber, userName
import requests
import time


def daily_stream():
    Watchlist = pd.read_csv('WatchList.csv')
    data = {}
    for Ticker in Watchlist:
        data[Ticker] = pd.read_csv(Ticker + '_' + 'Stream' + '_' + Date + '.csv')
    print(data)

Date = time.strftime('%Y-%m-%d', time.localtime()) 
daily_stream()