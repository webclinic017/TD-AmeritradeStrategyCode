import tkinter as tk 
from Client_ import TDClient
from config import client_id, password, accntNmber, userName
import os
TDSession = TDClient(account_number = accntNmber,
                     account_password = password,
                     redirect_uri = 'http://localhost/',
                     consumer_id = client_id,
                     #cache_state = True
                     )
class Application(tk.Frame):
    def _init_(self, master=None):
        tk.Frame._init_(self,master)
        self.master = master
        self.pack()
        self.init_window()
    def init_window(self):
        self.master.title('TD Ameritrade Trading Bot')
        self.pack(fill=BOTH, expand=1)
        self.buyButton = tk.Button(self, text='Buy Position')
        self.buyButton.pack(side='bottom')
        #self.symbols = TDSession.multiple_symbol_watchlist()
root = tk.Tk()
app = Application(master=root)
app.mainloop()