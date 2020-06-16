import matplotlib.pyplot as plt
import pandas as pd
import csv
from matplotlib.animation import FuncAnimation
import matplotlib
import os
from config import client_id, password, accntNmber, userName
import requests
import time
from Client_ import TDClient
import mpl_finance


TDPlot = TDClient(account_number = accntNmber,
                  account_password = password,
                  redirect_uri = 'http://localhost/',
                  consumer_id = client_id,
                  )
symbol = TDPlot.multiple_symbol_watchlist()
Date = time.strftime('%Y-%m-%d', time.localtime()) 








