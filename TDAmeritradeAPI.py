import requests
import os
from config import client_id, accntNmber, password
import time
from TDameritrade_authorization import TDAuthentication
import pandas as pd

seconds = time.time()

class Historical_Data(object):
    def __init__(self,client_id):
        self.client_id = client_id

    def Historical_Endpoint(self):
        #Historical Data

        # daily proces endpoint
        historicalEndpoint = r'https://api.tdameritrade.com/v1/marketdata/{}/pricehistory'.format('RING')

        # define a payload
        historicalPayload = {'apikey':client_id,
                   'periodType':'day',
                   'frequencytype':'minute',
                   'frequency':'1',
                   'period':'2',
                   'endDate':'1578448929',
                   'startDate':'1262311329', #Saturday, January 1, 2000 8:56:44 PM 
                   'needExtendedHoursData':'true'}

        # make a request
        historicalContent = requests.get(url = historicalEndpoint, params = historicalPayload)

        # convert it to a dictionary
        historicalData = historicalContent.json()
        print(historicalData)

class Quote(object):
    def __init__(self,client_id):
        self.client_id = client_id

    def Quotes(self):
        #Quotes

        # daily proces endpoint
        quoteEndpoint = r'https://api.tdameritrade.com/v1/marketdata/quotes'

        # define a payload
        quotePayload = {'apikey':client_id,
                        'symbol':'AVEO'
                       }


        # make a request
        quoteContent = requests.get(url = quoteEndpoint, params = quotePayload)

        # convert it to a dictionary
        quoteData = quoteContent.json()
        dfquoteData = pd.DataFrame.from_dict(quoteData)
        print(dfquoteData)
        price = dfquoteData['askPrice']
        print(price)
        #quoteDataKeys = quoteData.keys()
        #print(quoteDataKeys)

class Movers(object):
    def __init__(self,client_id):
        self.client_id = client_id

    def Movers(self):
        #Movers
        moverEndpoint = r'https://api.tdameritrade.com/v1/marketdata/{}/movers'.format('$SPX.X')

        # define a payload
        moverPayload = {'apikey':client_id,
                        'direction':'up',
                        'change':'value'
                        }

        # make a request
        moverContent = requests.get(url = moverEndpoint, params = moverPayload)

        # convert it to a dictionary
        moverData = moverContent.json()
        print(moverData)

        df_movers = pd.DataFrame.from_dict(moverData)

class Account_Data(object):
    def __init__(self,client_id,accntNmber,password):
        self.client_id = client_id
        self.accntNmber = accntNmber
        self.password = password

    def Account_Balance(self):

        #Endpoint
        AccntEndpoint = r'https://api.tdameritrade.com/v1/accounts/{}'.format(accntNmber)

        #Authorization
        TDClient = TDAuthentication(client_id, accntNmber, password)
        TDClient.authenticate()
        access_token = TDClient.access_token

        params = {'fields':'positions,orders'}
        headers = {'Authorization': 'Bearer {}'.format(access_token)}


        AccntContent = requests.get(url = AccntEndpoint, params = params, headers = headers)

        AccntData = AccntContent.json()
        dfAccntData = pd.DataFrame.from_dict(AccntData)
        print(dfAccntData)

class WatchList(object):
    def __init__(self,client_id,accntNmber,password):
        self.client_id = client_id
        self.accntNmber = accntNmber
        self.password = password

    def Watch_List(self):

        WatchListEndpoint = r'https://api.tdameritrade.com/v1/accounts/{}/watchlists'.format(accntNmber)

        #Authorization
        TDClient = TDAuthentication(client_id, accntNmber, password)
        TDClient.authenticate()
        access_token = TDClient.access_token

        headers = {'Authorization': 'Bearer {}'.format(access_token)}

        WatchListContent = requests.get(url = WatchListEndpoint, headers = headers)
        WatchListData = WatchListContent.json()
        print(WatchListData)
   




        

       