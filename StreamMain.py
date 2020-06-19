from Client_ import TDClient
from config import client_id, password, accntNmber, userName

#initialize new session with accnt info and caching false
TDSession = TDClient(account_number = accntNmber,
                     account_password = password,
                     redirect_uri = 'http://localhost/',
                     consumer_id = client_id,
                     #cache_state = True
                     )
TDSession.login()
print(TDSession.state['loggedin'])
print(TDSession.authstate)
symbol = TDSession.multiple_symbol_watchlist()
TDStreamer = TDSession.create_streaming_session()
TDStreamer.CSV_APPEND_MODE = True
lvlOneQuotes = TDStreamer.level_one_quote(symbols=symbol, fields=['0','1','2','3'])
Stream = TDStreamer.stream()