from Client_ import TDClient
from config import client_id, password, accntNmber, userName
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
import time
import os
TDSession = TDClient(account_number = accntNmber,
                     account_password = password,
                     redirect_uri = 'http://localhost/',
                     consumer_id = client_id,
                     #cache_state = True
                     )
TDSession.login()
print(TDSession.state['loggedin']) 
print(TDSession.authstate)
symbol = TDSession.multiple_symbol_watchlist()
tickers = st.sidebar.selectbox('Tickers in Watchlist', (symbol))
header = st.header(tickers)
data = {}
Date = time.strftime('%Y-%m-%d', time.localtime())
os.chdir('C:\SourceCode\TD-AmeritradeAPI\Data' + '\\' + Date + '\\' + 'OHLC')
data = pd.read_csv((tickers + '_' + 'OHLC' + '_' + Date + '.csv'))
st.dataframe(data)

