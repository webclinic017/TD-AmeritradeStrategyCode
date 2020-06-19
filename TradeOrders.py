from Client_ import TDClient
from Stream import TDStreamerClient
from config import client_id, password, accntNmber, userName
import json
import requests
import asyncio
import datetime
from typing import List

class TDOrders():
    def __init__(self, account_number, account_password, consumer_id, redirect_uri):
        self.session: TDClient = self._create_session()
    def _create_session(self, TDSession=None) -> TDClient:
        TDSession = TDClient(account_number = accntNmber,
                            account_password = password,
                            redirect_uri = 'http://localhost/',
                            consumer_id = client_id,
                            )
        TDSession.login()
        return TDSession
    def headers(self, mode=None, token=None) -> dict:
        token = self.state['access_token']
        headers = {'Authorization': 'Bearer {token}'.format(token = self.state['access_token'])}
        if mode == 'application/json':
            headers['Content-Type'] = 'application/json'
        if mode == 'json':
            headers['Content-Type'] = 'application/json'
        return headers
    def MarketOrder(self):
        Order = {"orderType": "MARKET",
                 "session": "NORMAL",
                 "duration": "DAY",
                 "orderStrategyType": "SINGLE",
                 "orderLegCollection": [{"instruction": "Buy",
                                                        "quantity": 1,
                                                        "instrument": {"symbol": "AVEO",
                                                                       "assetType": "EQUITY"
                                                                      }
                                        }
                                       ]
                }
        placeOrder = json.dumps(Order)
        return placeOrder
    def place_order(self, accntNmber=None, mode=None, TDSession=None):
        headers = self.headers(mode='json')
        orderData = self.MarketOrder()
        orderEndpoint = r'https://api.tdameritrade.com/v1/accounts/{}/orders'.format(accntNmber)
        PlaceOrder = requests.post(url=orderEndpoint, headers=headers, data=orderData)
        return PlaceOrder
