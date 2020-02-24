from Client_ import TDClient
from config import client_id, password, accntNmber, userName
from MathematicalTools import StatisticalTools



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
TDStreamer = TDSession.create_streaming_session()
TDStreamer.level_two_quotes(symbols = ['IBM'],fields=['0','1','2'])
TDStreamer.stream()
