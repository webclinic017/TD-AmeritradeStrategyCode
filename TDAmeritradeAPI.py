import requests
from config import client_id

class Historical_Data(object):
    def __init__(self,client_id):
        self.client_id = client_id
    def Historical_Endpoint(self):
        #Historical Data

        # daily proces endpoint
        historicalEndpoint = r'https://api.tdameritrade.com/v1/marketdata/{}/pricehistory'.format('AVEO')

        # define a payload
        historicalPayload = {'apikey':client_id,
                   'periodType':'day',
                   'frequencytype':'minute',
                   'frequency':'1',
                   'period':'2',
                   'endDate':'1576374829000',
                   'startDate':'1576029229000',
                   'needExtendedHoursData':'true'}

        # make a request
        historicalContent = requests.get(url = historicalEndpoint, params = historicalPayload)

        # convert it to a dictionary
        historicalData = historicalContent.json()
        print(historicalData)

def Quotes():
    #Quotes

    # daily proces endpoint
    quoteEndpoint = r'https://api.tdameritrade.com/v1/marketdata/quotes'

    # define a payload
    quotePayload = {'apikey':client_id,
                    'symbol':symbol
                   }


    # make a request
    quoteContent = requests.get(url = quoteEndpoint, params = quotePayload)

    # convert it to a dictionary
    quoteData = quoteContent.json()
    print(quoteData)

def Movers():
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
