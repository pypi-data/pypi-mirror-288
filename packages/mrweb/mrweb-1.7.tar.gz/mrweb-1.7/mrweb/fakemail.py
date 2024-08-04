from .exceptions import *
import requests
import json
from urllib.parse import urlencode

class FAKEMAIL:
    def __init__(self):
        self.version = "1.7"
    def create(self):
        return json.loads(requests.get("https://mrapiweb.ir/api/fakemail.php?method=getNewMail").text)["results"]["email"]
    def getmails(self,email):
        return json.loads(requests.get(f"https://mrapiweb.ir/api/fakemail.php?method=getMessages&email={email}").text)["results"]
