import requests
import asyncio
import datetime
import json
import pprint
import signal
import urllib
import dateutil.parser
import websockets
from Fields import STREAM_FIELD_IDS, STREAM_FIELD_KEYS

class TDStreamerClient(object):


    def __init__(self,websocket_url=None, user_principal_data=None, credentials=None):
        self.websocket_url = "wss://{}/ws".format(websocket_url)
        self.credentials = credentials
        self.user_principal_data = user_principal_data
        self.connection = None
        self.data_requests = {'requests': []}
        self.fields_ids_dictionary = STREAM_FIELD_IDS
        self.fields_keys_dictionary = STREAM_FIELD_KEYS 


    def _build_login_request(self):
            login_request = {'requests': [{'service': 'ADMIN',
                                   'command': 'LOGIN',
                                   'requestid': '0',
                                   'account': self.user_principal_data['accounts'][0]['accountId'],
                                   'source': self.user_principal_data['streamerInfo']['appId'],
                                   'parameters':{'credential': urllib.parse.urlencode(self.credentials),
                                                 'token': self.user_principal_data['streamerInfo']['token'],
                                                 'version': '1.0'
                                                }
                                   }
                                  ]
                            }
            return json.dumps(login_request)

    def set_default(self,obj):
        if isinstance(obj, set):
            return list(obj)
    def stream(self):
        login_request = self._build_login_request()
        data_request = json.dumps(self.data_requests, default=self.set_default)        
        self.loop = asyncio.get_event_loop()
        connection = self.loop.run_until_complete(self._connect())
        tasks = [asyncio.ensure_future(self._receive_message(connection)),
                 asyncio.ensure_future(self._send_message(login_request)),
                 asyncio.ensure_future(self._send_message(data_request))
                ]
        self.loop.run_until_complete(asyncio.wait(tasks))
    def close_stream(self):
        request = self._new_requst_template()
        request = self._new_requst_template()
        request['service'] = 'ADMIN'
        request['command'] = 'LOGOUT'
        request['parameters']['account'] = self.user_principal_data['accounts'][0]['accountId']
        task = asyncio.ensure_future(self._send_message(request))
        self.loop.run_until_complete(asyncio.wait(task))
        self.connection.close()
    async def _connect(self):
        self.connection = await websockets.client.connect(self.websocket_url)
        if self._check_connection():
            return self.connection
    def _check_connection(self):
        if self.connection.open:
            print('Connection established. Streaming will begin shortly.')
            return True
        else:
            raise ConnectionError
    async def _send_message(self, message=None):
        await self.connection.send(message)
    async def _receive_message(self, connection):
        while True:
            try:
                message = await self.connection.recv()
                try:
                    message_decoded = json.loads(message)
                    if 'data' in message_decoded.keys():
                        data = message_decoded['data'][0]
                        print(data)
                except:
                    message_decoded = message
                print('-'*20)
                print('Received message from server: ' + str(message_decoded))
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break
    async def heartbeat(self, connection):
        while True:
            try:
                await connection.send('ping')
                await asyncio.sleep(5)
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break
    def _new_request_template(self):
        service_count = len(self.data_requests['requests']) + 1
        request = {"service": None, "requestid": service_count, "command": None,
                   "account": self.user_principal_data['accounts'][0]['accountId'],
                   "source": self.user_principal_data['streamerInfo']['appId'],
                   "parameters": {"keys": None, "fields": None}}
        return request
    def _validate_argument(self, argument=None, endpoint=None):
        if isinstance(argument, list):
            arg_list = []
            for arg in argument:
                if isinstance(arg, int) and str(arg) in self.fields_ids_dictionary[endpoint]:
                    arg_list.append(str(arg))
                elif isinstance(arg, str) and arg in self.fields_keys_dictionary[endpoint]:
                    arg_list.append(str(self.fields_keys_dictionary[endpoint][arg]))
            return arg_list
        else:
            if isinstance(argument, int) and str(argument) in self.fields_ids_dictionary[endpoint]:
                argument = str(argument)
                return argument
            elif isinstance(argument, str) and argument in self.fields_keys_dictionary[endpoint]:
                argument = self.fields_keys_dictionary[endpoint][argument]
                return argument
            else:
                return None
    def quality_of_service(self, qos_level=None):
        qos_level = self._validate_argument(argument=qos_level, endpoint='qos_request')
        if qos_level is not None:
            request = self._new_request_template()
            request['service'] = 'ADMIN'
            request['command'] = 'QOS'
            request['parameters']['qoslevel'] = qos_level
            self.data_requests['requests'].append(requests)
        else:
            raise ValueError('Error')

    def level_two_quotes(self, symbols=None, fields=None):
        request = self._new_request_template()
        request['service'] = 'LISTED_BOOK'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)
        self.data_requests['requests'].append(request)

