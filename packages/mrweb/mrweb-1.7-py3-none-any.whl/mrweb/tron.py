from .exceptions import *
import requests
import json
from urllib.parse import urlencode
from os import environ

class TRON:
    def __init__(self):
        self.version = "1.7"
    def generate(self):
        api=json.loads(requests.get("https://mrapiweb.ir/api/tronapi.php?action=genaddress").text)
        return api
    def balance(self,address):
        api=json.loads(requests.get(f"https://mrapiweb.ir/api/tronapi.php?action=getbalance&address={address}").text)
        return api["balance"]
    def info(self,address):
        api=json.loads(requests.get(f"https://mrapiweb.ir/api/tronapi.php?action=addressinfo&address={address}").text)
        return api
    def send(self,key,fromadd,to,amount):
        api=json.loads(requests.get(f"https://mrapiweb.ir/api/tronapi.php?action=sendtrx&key={key}&fromaddress={fromadd}&toaddress={to}&amount={amount}").text)
        return api
