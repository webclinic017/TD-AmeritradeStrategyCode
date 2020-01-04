import requests 
from config import password, accntNmber, client_id
from TDAmeritradeAPI import Historical_Data

TD_HistoricalAPI = Historical_Data(client_id)
TD_HistoricalAPI.Historical_Endpoint()