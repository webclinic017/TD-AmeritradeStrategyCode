import requests 
import json
from config import password, accntNmber, client_id
from TDAmeritradeAPI import Historical_Data
from TDAmeritradeAPI import Quote
from TDAmeritradeAPI import Account_Data
from TDAmeritradeAPI import WatchList
from DataStream import Main_Runtime
from TDameritrade_authorization import TDAuthentication


#TD_WatchList = WatchList(client_id,accntNmber,password)
#TD_WatchList.Watch_List()

TD_QuoteAPI = Quote(client_id)
TD_QuoteAPI.Quotes()


#Login and Access Account
#TDClient = TDAuthentication(client_id, accntNmber, password)
#TDClient.authenticate()
#access_token = TDClient.access_token

#TD_AccntData = Account_Data(client_id,accntNmber,password)
#TD_AccntData.Account_Balance()

#TD_HistoricalAPI = Historical_Data(client_id)
#TD_HistoricalAPI.Historical_Endpoint()






