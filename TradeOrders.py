from Client_ import TDClient
from config import client_id, password, accntNmber, userName
import json
import requests

TDSession = TDClient(account_number = accntNmber,
                     account_password = password,
                     redirect_uri = 'http://localhost/',
                     consumer_id = client_id,
                    )
TDSession.login()
symbol = TDSession.multiple_symbol_watchlist()
AccntInfo = TDSession.accounts(accntNmber=accntNmber)
def MarketOrder():
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
def place_order(accntNmber=None, mode=None):
    headers = TDSession.headers(mode='json')
    orderData = MarketOrder()
    orderEndpoint = r'https://api.tdameritrade.com/v1/accounts/{}/orders'.format(accntNmber)
    PlaceOrder = requests.post(url=orderEndpoint, headers=headers, data=orderData)
    return PlaceOrder