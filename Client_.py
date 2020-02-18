from config import client_id,accntNmber,password,redirect_uri
from TDameritrade_authorization import TDAuthentication
import urllib.parse
from urllib.parse import urlparse
import urllib3
import uuid
import os
import json
import requests
import dateutil.parser
from datetime import datetime

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
                raise KeyErro('Invalid Argument Name.')
        self.config.update(kwargs.items())
        self.state_manager('init')

        self.authstate = ''

    def __repr__(self):
        if self.state['loggedin']:
            logged_in_state = 'True'
        else:
            logged_in_state = 'False'

        str_representation = '<TDAmeritrade Client (logged_in = {}, authorized = {})>'.format('TRUE', self.config['consumer_id'])
        return str_representation

    def headers(self):
        token = self.state['access_token']
        headers = {'Authorization':f'Bearer {token}'}
        return headers

    def api_endpoint(self, url):
        if urllib.parse.urlparse(url).scheme in ['http', 'https']:
            return url
        return urllib.parse.urljoin(self.config['resource'] + self.config['api_version'] + '/',urllstrip('/'))

    def state_manager(self, action):
        initialized_state = {'access_token': None,
                             'refresh_token': None,
                             'token_expires_at': 0,
                             'authorization_url': '',
                             'redirect_code': None,
                             'token_scope': '',
                             'loggedin': False}
        dir_path = r'C:\Dan\Projects\TD_API\TD-AmeritradeStrategyCode'
        filename = 'TDAmeritradeState.json'
        file_path = os.path.join(dir_path, filename)
        if action == 'init':
            self.state = initialized_state
            if self.config['cache_state'] and os.path.isfile(filename):
                with open(filename, 'r') as fileHandle:
                    self.state.update(json.load(fileHandle))
            elif not self.config['cache_state'] and os.path.isfile(filename):
                os.remove(filename)
        elif action == 'save' and self.config['cache_state']:
            with open(filfilename, 'w') as fileHandle:
                json_string = {key:self.state[key] for key in initialized_state}
                json.dump(json_string, fileHandle)
    def login(self):
        if self.config['cache_state']:
            if self.silent_sso():
                return True
        self.authstate = 'Authenticated'
        client_code = client_id + '@AMER.OAUTHAP'
        payload = {'response_type':'code',
                   'redirect_uri':'http://localhost/',
                   'client_id':client_code}
        params = urllib.parse.urlencode(payload)
        url = self.config['auth_endpoint'] + params
        self.state['authorization_url'] = url
        TDAuthentication(client_id,accntNmber,password)
        TDAuthentication._get_access_code(self)
        TDAuthentication.authenticate(self)
        my_response = input('Paste the full URL resirect here: ')
        #print('Please go to url provided authorize your account: {}'.format(self.state['authorization_url']))
        self.state['redirect_code'] = my_response
        self.grab_access_token()
    def logout(self):
        self.state_manager('init')
    def grab_access_token(self):
        url_dict = urllib.parse.parse_qs(self.state['redirect_code'])
        url_values = list(url_dict.values())
        url_code = url_values[0][0]
        data = {'grant_type':'authorization_code',
                'client_id':client_id,
                'access_type':'offline',
                'code':url_code,
                'redirect_uri':'http://localhost/'
               }
        token_response = requests.post(url = self.config['token_endpoint'], data=data, verify=True)
        self.token_save(token_response)
        if token_response and token_response.ok:
            self.state_manager('save')
    def silent_sso(self):
        if self.tokem_seconds() > 0:
            return True
        
        elif self.state['refresh_token']:
            self.token_refresh()
            return True
        return False
    def token_refresh(self):
        data = {'grant_type':'refresh_token',
                'client_id':client_id,
                'refresh_token':self.state['refresh_token']
               }
        response = requests.post(url = self.config['token_endpoint'], data=data, verify=True)
        self.token_save(response)
    def token_save(self, response):
        json_data = response.json()
        if 'access_token' not in json_data:
            self.logout()
            return False
        self.state['access_token'] = json_data['access_token']
        self.state['loggedin'] = True
        self.state['token_expires_at'] = time.time() + int(json_data['expires_in'])
        self.state['refresh_token'] = json_data['refresh_token']
    def token_seconds(self):
        if not self.state['access_token'] or time.time() >= self.state['token_expires_at']:
            return 0 
        return int(self.state['token_expores_at']-time.time())
    def token_validation(self, nseconds = 5):
        if self.token_seconds() < nseconds and self.config['refresh_enabled']:
            self.token_refresh()
        


