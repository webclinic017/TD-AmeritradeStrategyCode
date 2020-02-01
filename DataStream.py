import urllib
import json
import requests
import dateutil.parser
from datetime import datetime
from TDameritrade_authorization import TDAuthentication
from config import password, accntNmber, client_id
import websockets
import asyncio
import pyodbc
import nest_asyncio
nest_asyncio.apply()


class Main(object):
    import datetime
    def unix_time_millis(dt):

        epoch = datetime.datetime.utcfromtimestamp(0)
        return (dt - epoch).total_seconds() * 1000

    TDClient = TDAuthentication(client_id, accntNmber, password)
    TDClient.authenticate()
    access_token = TDClient.access_token

    # User Principles endpoint
    endpoint = r'https://api.tdameritrade.com/v1/userprincipals'
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    params = {'fields':'streamerSubscriptionKeys,streamerConnectionInfo'}

    #make a request
    content = requests.get(url = endpoint, params = params, headers = headers)
    userPrincipalsResponse = content.json()

    #grab the timestamp and conver to ms
    tokenTimeStamp = userPrincipalsResponse['streamerInfo']['tokenTimestamp']
    date = dateutil.parser.parse(tokenTimeStamp, ignoretz = True)
    tokenTimeStampAsMs = unix_time_millis(date)


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

    login_request = {'requests': [{'service': 'ADMIN',
                                   'command': 'LOGIN',
                                   'requestid': '0',
                                   'account': userPrincipalsResponse['accounts'][0]['accountId'],
                                   'source': userPrincipalsResponse['streamerInfo']['appId'],
                                   'parameters':{'credential': urllib.parse.urlencode(credentials),
                                                 'token': userPrincipalsResponse['streamerInfo']['token'],
                                                 'version': '1.0'
                                                }
                                   }
                                  ]
                    }

    data_requests = { "requests": [{'service': 'Quotes', 
                                    'requestid': '2', 
                                    'command': 'SUBS', 
                                    'account': userPrincipalsResponse['accounts'][0]['accountId'],
                                    'source': userPrincipalsResponse['streamerInfo']['appId'], 
                                    'parameters': {'keys': 'AAPL,MSFT', 
                                                   'fields': '0,1,2,3,4'
                                                  }
                                    }
                                   ]
                     }
    
    #turn request to json string
    login_encoded = json.dumps(login_request)
    data_encoded = json.dumps(data_requests)


    class WebSocketClient():

        def __init__(self):
            self.cnxn = None
            self.crsr = None

        def database_connect(self):
            server = 'DESKTOP-0NIEKNL\SQLEXPRESS'
            database = 'stock_database'
            sql_driver = '{ODBC Driver 17 for SQL Server}'
            self.cnxn = pyodbc.connect(driver = sql_driver,
                                       server = server,
                                       database = database,
                                       trusted_connection = 'yes',
                                       autocommit = True)
            self.crsr = self.cnxn.cursor()

        async def database_insert(self, query, data_tuple): 
            try:
                self.crsr.execute(query, data_tuple)
                self.cnxn.commit()
            except Exception as e:
                print(e)
            finally:
                self.cnxn.close()
                print('Data has been Succesfully inserted')

        async def connect(self):
            uri = 'wss://' + userPrincipalsResponse['streamerInfo']['streamerSocketUrl'] + '/ws'
            self.connection = await websockets.client.connect(uri)
            if self.connection.open:
                print('Connection Established. Client correctly connected')
                return self.connection

        async def sendMessage(self, message):
            await self.connection.send(message)

        async def recieveMessage(self, connection):
            while True:
                try:
                    message = await connection.recv()
                    message_decoded = json.loads(message) 
                    query = 'INSERT INTO td_service_data (service, timestamp, command) VALUES (?,?,?);'
                    self.database_connect()
                    if 'data' in message_decoded.keys():
                        data = message_decoded['data'][0]
                        data_tuple = (data['service'], data['timestamp'], data['command'])  
                        self.database_insert(query, data_tuple)
                    print('-'*20)
                    print('Recieved message from server ' + str(message))
                    #else:
                       # print('No data')
                except websockets.exceptions.ConnectionClosed:
                    print('Connection with server is closed')
                    break

        async def heartbeat(self, connection):
            while True:
                try:
                    await connection.send('ping')
                    await asyncio.sleep(5)
                except websockets.exceptions.ConnectionClosed:
                    print('Connection to server was closed')
                    break
        def __init__(self):
            self.cnxn = None
            self.crsr = None

    def MainLoop():
        if __name__ == '__main__':
            client = WebSocketClient()
            loop = asyncio.get_event_loop()
            connection = loop.run_until_complete(client.connect())
            tasks = [asyncio.ensure_future(client.recieveMessage(connection)),
                     asyncio.ensure_future(client.sendMessage(login_encoded)),
                     asyncio.ensure_future(client.recieveMessage(connection)),
                     asyncio.ensure_future(client.sendMessage(data_encoded)),
                     asyncio.ensure_future(client.recieveMessage(connection)),]
            loop.run_until_complete(asyncio.wait(tasks))