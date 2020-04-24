from Client_ import TDClient
from config import client_id, password, accntNmber, userName
from datetime import datetime
from datetime import timedelta
import json
#Inputs
#
Num_DayMAInputs = 40
symbol = 'USO'
#
#initialize new session with accnt info and caching false
TDSession = TDClient(account_number = accntNmber,
                      account_password = password,
                      redirect_uri = 'http://localhost/',
                      consumer_id = client_id,
                      cache_state = True
                     )
TDSession.login()
print(TDSession.state['loggedin'])
print(TDSession.authstate)
#Method1: Bollinger Bands
#
#Define parameters for Candles Data Open High Low Close (OHLC)
hist_endDate = str(int(round(datetime.now().timestamp() * 1000)))
hist_symbol = symbol
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
#
#Start Straming Session
TDStreamer = TDSession.create_streaming_session()
TDStreamer.CSV_APPEND_MODE = True
TDStreamer.level_one_quote(symbols=[symbol], fields=['0','1','2','3'])
TDStreamer.stream()
