import tkinter 
from tkinter import *
from Client_ import TDClient
from config import client_id, password, accntNmber, userName
import os

Font_large = ('Verdana', 12)
'''
TDSession = TDClient(account_number = accntNmber,
                     account_password = password,
                     redirect_uri = 'http://localhost/',
                     consumer_id = client_id,
                     #cache_state = True
                     )
'''
class Application(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        #tk.Frame.__init__(self, parent, *args, **kwargs)
        self.master = master
        master.title("A simple GUI")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

root = tk.Tk()
Application(root)
root.mainloop()