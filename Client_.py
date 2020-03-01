from config import client_id,accntNmber,password,redirect_uri
from TDameritrade_authorization import TDAuthentication
from Stream import TDStreamerClient
import urllib.parse
from urllib.parse import urlparse
import urllib3
import uuid
import os
import json
import requests
import dateutil.parser
from datetime import datetime
import time

class TDClient():

    def __init__(self,**kwargs):
        self.config = {'consumer_id': client_id,
                       'account_number': accntNmber,
                       'account_password': password,
                       'redirect_uri': redirect_uri,
                       'resource': 'https://api.tdameritrade.com',
                       'api_version': '/v1',
                       'cache_state': True,
                       'authenticaiton_url': 'https://auth.tdameritrade.com',
                       'auth_endpoint': 'https://auth.tdameritrade.com' + '/auth?',
                       'token_endpoint': 'https://api.tdameritrade.com' + '/v1' + '/oauth2/token',
                       'refresh_enabled': True
                       }
        self.endpoint_arguments = {'search_instruments': {'projection': ['symbol-search', 'symbol-regex', 'desc-search', 'desc-regex', 'fundamental']},
                                   'get_market_hours': {'markets': ['EQUITY', 'OPTION', 'FUTURE', 'BOND', 'FOREX']},
                                   'get_movers': {'market': ['$DJI', '$COMPX', '$SPX.X'],
                                                  'direction': ['up', 'down'],
                                                  'change': ['value', 'percent']},
                                   'get_user_principals': {'fields': ['streamerSubscriptionKeys', 'streamerConnectionInfo', 'preferences', 'surrogateIds']}
                                  }
        for key in kwargs:
            if key not in self.config:
                print('Warning: the argument {} is an unknown argument'.format(key))
                raise KeyError('Invalid Argument Name.')
        self.config.update(kwargs.items())
        self.state_manager('init')

        self.authstate = False

    def __repr__(self):
        if self.state['loggedin']:
            logged_in_state = 'True'
        else:
            logged_in_state = 'False'

        str_representation = '<TDAmeritrade Client (logged_in = {}, authorized = {})>'.format(logged_in_state, self.authstate)
        return str_representation
    def headers(self, mode=None):
        token = self.state['access_token']
        headers = {'Authorization':f'Bearer {token}'}
        if mode == 'application/json':
            headers['Content-type'] = 'application/json'
        return headers
    def api_endpoint(self, url):
        if urllib.parse.urlparse(url).scheme in ['http', 'https']:
            return url
        return urllib.parse.urljoin(self.config['resource'] + self.config['api_version'] + '/', url.lstrip('/'))
    def state_manager(self, action):
        initialized_state = {'access_token': None,
                             'refresh_token': None,
                             'access_token_expires_at': 0,
                             'refresh_token_expires_at': 0,
                             'authorization_url': None,
                             'redirect_code': None,
                             'token_scope': '',
                             'loggedin': False}
        dir_path = os.path.dirname(os.path.realpath(__file__))
        #dir_path = r'C:\Dan\Projects\TD_API\TD-AmeritradeStrategyCode'
        filename = 'TDAmeritradeState.json'
        file_path = os.path.join(dir_path, filename)
        if action == 'init':
            self.state = initialized_state
            if self.config['cache_state'] and os.path.isfile(file_path):
                with open(file_path, 'r') as fileHandle:
                    self.state.update(json.load(fileHandle))
            elif not self.config['cache_state'] and os.path.isfile(os.path.join(dir_path,filename)):
                os.remove(file_path)
        elif action == 'save' and self.config['cache_state']:
            with open(file_path, 'w') as fileHandle:
                json_string = {key:self.state[key] for key in initialized_state}
                json.dump(json_string, fileHandle)
    def login(self):
        if self.config['cache_state']:
            if self.silent_sso():
                self.authstate = 'Authenticated'
                return True
        self.authstate = 'Authenticated'
        payload = {'response_type':'code',
                   'redirect_uri':'http://localhost/',
                   'client_id':self.config['consumer_id'] + '@AMER.OAUTHAP'}
        params = urllib.parse.urlencode(payload)
        url = self.config['auth_endpoint'] + params
        self.state['authorization_url'] = url
        #TDAuthentication(client_id,accntNmber,password)
        #TDAuthentication._get_access_code(self)
        #TDAuthentication.authenticate(self)
        print('Please go to url provided authorize your account: {}'.format(self.state['authorization_url']))
        my_response = input('Paste the full URL resirect here: ')
        self.state['redirect_code'] = my_response
        self.grab_access_token()
    def logout(self):
        self.state_manager('init')
    def grab_access_token(self):
        url_dict = urllib.parse.parse_qs(self.state['redirect_code'])
        url_values = list(url_dict.values())
        url_code = url_values[0][0]
        data = {'grant_type':'authorization_code',
                'client_id':self.config['consumer_id'],
                'access_type':'offline',
                'code':url_code,
                'redirect_uri':'http://localhost/'
               }
        token_response = requests.post(url = self.config['token_endpoint'], data=data, verify=True)
        self.token_save(token_response)
        if token_response and token_response.ok:
            self.state_manager('save')
    def silent_sso(self):
        if self.token_seconds(token_type='access_token') > 0:
            return True
        elif self.token_seconds(token_type='refresh_token') <= 0:
            return False
        elif self.state['refresh_token'] and self.token_refresh():
            return True
        return False
    def token_refresh(self):
        data = {'grant_type':'refresh_token',
                'client_id':self.config['consumer_id'] + '@AMER.OAUTHAP',
                'refresh_token':self.state['refresh_token'],
                'access_type':'offline'
               }
        response = requests.post(url = self.config['token_endpoint'], data=data, verify=True)
        if response.status_code == 401:
            print('The Credentials you passed through are invalid.')
            return False
        elif response.status_code == 400:
            print('Validation was unsuccessful.')
            return False
        elif response.status_code == 500:
            print('The TD Server is experiencing an error, please try again later.')
            return False
        elif response.status_code == 403:
            print("You don't have access to this resource, cannot authenticate.")
            return False
        elif response.status_code == 503:
            print("The TD Server can't respond, please try again later.")
            return False
        else:
            self.token_save(response)
            self.state_manager('save')
            return True
    def token_save(self, response):
        json_data = response.json()
        if 'access_token' not in json_data:
            self.logout()
            return False
        self.state['access_token'] = json_data['access_token']
        self.state['refresh_token'] = json_data['refresh_token']
        self.state['loggedin'] = True
        self.state['access_token_expires_at'] = time.time() + int(json_data['expires_in'])
        self.state['refresh_token_expires_at'] = time.time() + int(json_data['refresh_token_expires_in'])
        return True
    def token_seconds(self, token_type = 'access_token'):
        if token_type == 'access_token':
            if not self.state['access_token'] or time.time() >= self.state['access_token_expires_at']:
                return 0
            token_exp = int(self.state['access_token_expires_at'] - time.time())
        elif token_type == 'refresh_token':
            if not self.state['refresh_token'] or time.time() >= self.state['refresh_token_expires_at']:
                return 0
            token_exp = int(self.state['refresh_token_expires_at'] - time.time())
        return token_exp
    def token_validation(self, nseconds = 5):
        if self.token_seconds() < nseconds and self.config['refresh_enabled']:
            self.token_refresh()
    def _create_token_timestamp(self, token_timestamp = None):
        token_timestamp = datetime.strptime(token_timestamp, "%Y-%m-%dT%H:%M:%S%z")
        token_timestamp = int(token_timestamp.timestamp()) * 1000
        return token_timestamp
#
#
# CREATE STREAMING SESSION
    def validate_arguments(self, endpoint=None, parameter_name=None, parameter_argument=None):
        parameters_dictionary = self.endpoint_arguments[endpoint]
        parameter_possible_arguments = parameters_dictionary[parameter_name]
        if type(parameter_argument) is list:
            validation_result = [
                argument not in parameter_possible_arguments for argument in parameter_argument]
            if any(validation_result):
                print('\nThe value you passed through is not valid, please choose one of the following valid values: {} \n'.format(
                    ' ,'.join(parameter_possible_arguments)))
                raise ValueError('Invalid Value.')
            elif not any(validation_result):
                return True
        elif parameter_argument not in parameter_possible_arguments:
            print('\nThe value you passed through is not valid, please choose one of the following valid values: {} \n'.upper(
            ).format(' ,'.join(parameter_possible_arguments)))
            raise ValueError('Invalid Value.')
        elif parameter_argument in parameter_possible_arguments:
            return True
    def prepare_arguments_list(self, parameter_list=None):
        if type(parameter_list) is list:
            delimeter = ','
            parameter_list = delimeter.join(parameter_list)
        return parameter_list
    def get_quotes(self, instruments=None):
        self.token_validation()
        merged_headers = self.headers()
        instruments = self.prepare_arguments_list(parameter_list=instruments)
        data = {'apikey': self.config['consumer_id'],
                'symbol': instruments}
        endpoint = '/marketdata/quotes'
        url = self.api_endpoint(endpoint)
        return requests.get(url=url, headers=merged_headers, params=data, verify=True).json()
    def get_user_principals(self, fields=None):
        self.token_validation()
        self.validate_arguments(endpoint='get_user_principals',parameter_name='fields', parameter_argument=fields)
        merged_headers = self.headers()
        fields = self.prepare_arguments_list(parameter_list=fields)
        endpoint = '/userprincipals'
        data = {'fields': fields}
        url = self.api_endpoint(endpoint)
        return requests.get(url=url, headers=merged_headers, params=data, verify=True).json()
    def create_streaming_session(self):
        userPrincipalsResponse = self.get_user_principals(fields = ['streamerConnectionInfo'])
        tokenTimeStamp = userPrincipalsResponse['streamerInfo']['tokenTimestamp']
        socket_url = userPrincipalsResponse['streamerInfo']['streamerSocketUrl']
        tokenTimeStampAsMs = self._create_token_timestamp(token_timestamp=tokenTimeStamp)
        print(tokenTimeStamp, socket_url,tokenTimeStampAsMs)
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
        streaming_session = TDStreamerClient(websocket_url=socket_url, user_principal_data=userPrincipalsResponse,credentials=credentials)
        return streaming_session

      
