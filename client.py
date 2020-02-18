from TDameritrade_authorization import TDAuthentication
from config import client_id,accntNmber,password,redirect_uri
from Stream import TDStreamerClient
import urllib
import json
import requests
import dateutil.parser
from datetime import datetime

class TDClient():

    def __init__(self,**kwargs):


    def AccessTokenAuth():
        #Login and Access Account
        TDAuth = TDAuthentication(client_id, accntNmber, password)
        TDAuth.authenticate()
        access_token = TDAuth.access_token
        #print(access_token)

    def create_streaming_session():

        TDAuth = TDAuthentication(client_id, accntNmber, password)
        TDAuth.authenticate()
        access_token = TDAuth.access_token

        endpoint = r'https://api.tdameritrade.com/v1/userprincipals'
        headers = {'Authorization': 'Bearer {}'.format(access_token)}
        params = {'fields':'streamerSubscriptionKeys,streamerConnectionInfo'}

        #make a request
        content = requests.get(url = endpoint, params = params, headers = headers)
        userPrincipalsResponse = content.json()

        #grab the timestamp and conver to ms
        tokenTimeStamp = userPrincipalsResponse['streamerInfo']['tokenTimestamp']
        socket_url = userPrincipalsResponse['streamerInfo']['streamerSocketUrl']
        token_timestamp = dateutil.parser.parse(tokenTimeStamp, ignoretz = True)
        epoch = datetime.utcfromtimestamp(0)
        tokenTimeStampAsMs = int((token_timestamp - epoch).total_seconds() * 1000.0)


        #define items we need to make a request
        credentials = {'userid':userPrincipalsResponse['accounts'][0]['accountId'],
                       'token':userPrincipalsResponse['streamerInfo']['token'],
                       'company':userPrincipalsResponse['accounts'][0]['company'],
                       'segment':userPrincipalsResponse['accounts'][0]['segment'],
                       'cddomain':userPrincipalsResponse['accounts'][0]['accountCdDomainId'],
                       'usergroup':userPrincipalsResponse['streamerInfo']['userGroup'],
                       'accesslevel':userPrincipalsResponse['streamerInfo']['accessLevel'],
                       'authorized':'Y',
                       'timestamp':int(tokenTimeStampAsMs),
                       'appid':userPrincipalsResponse['streamerInfo']['appId'],
                       'acl':userPrincipalsResponse['streamerInfo']['acl'],
                       }
        streaming_session = TDStreamerClient(websocket_url=socket_url, user_principles_data=userPrincipalsResponse, credentials=credentials)

        print('it worked')

        return streaming_session






