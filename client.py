from TDameritrade_authorization import TDAuthentication
from config import client_id,accntNmber,password

class TDClient():

    def AccessTokenAuth():
        #Login and Access Account
        TDAuth = TDAuthentication(client_id, accntNmber, password)
        TDAuth.authenticate()
        access_token = TDAuth.access_token
        print(access_token)





