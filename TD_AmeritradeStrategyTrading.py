from Client_ import TDClient
from config import client_id, password, accntNmber, userName

#Method1:
#initialize new session with accnt info and caching false
TDSession = TDClient(account_number = accntNmber,
                      account_password = password,
                      redirect_uri = 'http://localhost/',
                      consumer_id = client_id
                     )
TDSession.login()

print(TDSession.state['loggedin'])

print(TDSession.authstate)