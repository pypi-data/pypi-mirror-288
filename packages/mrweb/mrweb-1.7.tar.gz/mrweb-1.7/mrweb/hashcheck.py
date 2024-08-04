from .exceptions import *
import requests
import json
from urllib.parse import urlencode

class HASHCHECK:
    def __init__(self):
        self.version = "1.7"
    def tron(self,thash):
        api=requests.get(f"https://mrapiweb.ir/api/cryptocheck/tron.php?hash={thash}").text
        tron=json.loads(api)
        return tron
    def tomochain(self,thash):
        api=requests.get(f"https://mrapiweb.ir/api/cryptocheck/tomochain.php?hash={thash}").text
        tomo=json.loads(api)
        return tomo
