import requests 
from client import TDClient
from config import accntNmber, password, client_id, redirect_uri


#TDClient.AccessTokenAuth()

# Create a streaming sesion
TDStreamingClient = TDClient.create_streaming_session()

TDStreamingClient.level_one_quotes(symbols=['MSFT','AAPL','TSLA'],  fields=list(range(0,53)))
#TD_QuoteAPI = Quote(client_id)
#TD_QuoteAPI.Quotes()








