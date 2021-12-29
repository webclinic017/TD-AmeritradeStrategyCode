import requests
import asyncio
import datetime
from datetime import datetime
import json
import pprint
import signal
import urllib
import dateutil.parser
import websockets
from Fields import STREAM_FIELD_IDS, CSV_FIELD_KEYS
import csv
import pandas as pd
import datetime
import time
import os
from os import path

class TDStreamerClient(object):
    def __init__(self, websocket_url=None, user_principal_data=None, credentials=None, write='csv', append_mode=True):
        self.websocket_url = "wss://{}/ws".format(websocket_url)
        self.credentials = credentials
        self.user_principal_data = user_principal_data
        self.connection = None
        self.data_requests = {'requests': []}
        self.fields_ids_dictionary = STREAM_FIELD_IDS
        self.fields_keys_write = CSV_FIELD_KEYS
        if append_mode == True:
            self.CSV_APPEND_MODE = True
        elif append_mode == False:
            self.CSV_APPEND_MODE = False
    def epoch_datetime(self):
        TimeDay = time.strftime('%Y-%m-%d', time.localtime()) 
        TimeSec = time.strftime('%I:%M:%S', time.localtime()) 
        return TimeDay   
    async def _write_stream_to_csv(self, data=None):
        num = data[0]['content']
        Sym = [i['key'] for i in num]
        SymNum = len(Sym)
        Date = self.epoch_datetime()
        TimeSec = time.strftime('%I:%M:%S', time.localtime()) 
        import os
        if path.exists('C:\SourceCode\TD-AmeritradeAPI\Data' + '\\' + Date + '\\' + 'StreamData'):                
           os.chdir('C:\SourceCode\TD-AmeritradeAPI\Data' + '\\' + Date + '\\' + 'StreamData')
           if self.CSV_APPEND_MODE == True:
               csv_write_mode = 'a+'
           else:
               csv_write_mode = 'w'             
           for i in range(SymNum):
               Symbol = data[0]['content'][i]['key']
               AskPrice = data[0]['content'][i]['3']          
               with open((Symbol + '_' + 'Stream' + '_' + Date + '.csv'), mode=csv_write_mode, newline='') as stream_file:           
                   stream_writer = csv.writer(stream_file)
                   print('writing')
                   data = [Symbol, AskPrice, TimeSec]
                   stream_writer.writerow(data)
        else:
            os.mkdir('C:\SourceCode\TD-AmeritradeAPI\Data' + '\\' + Date + '\\' + 'StreamData')
            os.chdir('C:\SourceCode\TD-AmeritradeAPI\Data' + '\\' + Date + '\\' + 'StreamData')
            if self.CSV_APPEND_MODE == True:
                csv_write_mode = 'a+'
            else:
                csv_write_mode = 'w'             
            for i in range(SymNum):
                Symbol = data[0]['content'][i]['key']
                AskPrice = data[0]['content'][i]['3']          
                with open((Symbol + '_' + 'Stream' + '_' + Date + '.csv'), mode=csv_write_mode, newline='') as stream_file:           
                    stream_writer = csv.writer(stream_file)
                    print('writing')
                    data = [Symbol, AskPrice, TimeSec]
                    stream_writer.writerow(data)
            #os.chdir('C:\SourceCode\TD-AmeritradeAPI')
    async def epoch_to_datetime(self, data=None, TimeSec=None):
        timestamp = data[0]['timestamp']
        TimeDay = time.strftime('%Y-%m-%d', time.localtime()) 
        TimeSec = time.strftime('%I:%M:%S', time.localtime()) 
        return TimeDay
        return TimeSec
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
        data_request = json.dumps(self.data_requests)#, default=self.set_default)        
        self.loop = asyncio.get_event_loop()
        connection = self.loop.run_until_complete(self._connect())
        asyncio.ensure_future(self._receive_message(connection)),
        asyncio.ensure_future(self._send_message(login_request)),
        asyncio.ensure_future(self._send_message(data_request))
        self.loop.run_forever()
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
        approved_writes = list(self.fields_keys_write.keys())
        while True:
            try:
                message = await self.connection.recv()
                try:
                    message_decoded = json.loads(message)
                    if 'data' in message_decoded.keys():
                        if message_decoded['data'][0]['service'] in approved_writes:
                            await self._write_stream_to_csv(data = message_decoded['data'])
                            #await self.symbol_numbers(data = message_decoded['data'])
                            await self.epoch_to_datetime(data = message_decoded['data'])
                except:
                    message_decoded = message
                print('-'*20)
                print('Received message from server: {}'.format(str(message_decoded)))
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
                arg_str = str(arg)
                key_list = list(self.fields_ids_dictionary[endpoint].keys())
                val_list = list(self.fields_ids_dictionary[endpoint].values())
                if arg_str in key_list:
                    arg_list.append(arg_str)
                elif arg_str in val_list:
                    key_value = key_list[val_list.index(arg_str)]
                    arg_list.append(key_value)                  
            return arg_list
        else:
            arg_str = str(argument)
            key_list = list(self.fields_ids_dictionary[endpoint].keys())
            val_list = list(self.fields_ids_dictionary[endpoint].values())
            if arg_str in key_list:
                arg_list.append(arg_str)
            elif arg_str in val_list:
                key_value = key_list[val_list.index(arg_str)]
                arg_list.append(key_value)
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
    def level_one_quote(self, symbols=None, fields=None):
        fields = self._validate_argument(argument=fields, endpoint='level_one_quote')
        request = self._new_request_template()
        request['service'] = 'QUOTE'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(str(v) for v in symbols)
        quoteData = request['parameters']['fields'] = ','.join(fields)
        self.data_requests['requests'].append(request)
    async def stream_Trader(self, data=None):
        TimeSec = time.strftime('%I:%M:%S', time.localtime())
        print(data)

