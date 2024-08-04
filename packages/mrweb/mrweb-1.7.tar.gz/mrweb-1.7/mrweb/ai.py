from .exceptions import *
import requests
import json
from urllib.parse import urlencode

from os import environ

class AI:
    def __init__(self):
        self.version = "1.7"
        
    def bard(self,query):
        try:
            result = requests.get("https://mrapiweb.ir/bardai/ask?text="+urlencode({"text":query})).text
            return result
        except Exception as er:
            raise AIError("Failed To Get Response From Bard") from er
    def gpt(self,query):
        
        query=urlencode({"text":query})
        try:
            return requests.get(f"https://mrapiweb.ir/ai/?{query}").text
        except Exception as er:
            raise AIError("Failed To Get Answer Make Sure That You Are Connected To Internet & vpn is off") from None
        
    def evilgpt(self,query):
        raise EndSupport("EvilGPT Is End Of Support") from None
    
    def gemini(self,query):
        query=urlencode({"query":query})
        api=requests.get(f"https://mrapiweb.ir/api/geminiai.php?{query}").text
        try:
            return api
        except:
            raise AIError("No Answer Found From Gemini. Please Try Again!") from None
    
    def codeai(self,query):
        query=urlencode({"query":query})
        api=requests.get(f"https://mrapiweb.ir/api/aiblack.php?{query}").text
        try:
            return api
        except:
            raise AIError("No Answer Found From CodeAI. Please Try Again!") from None

    def gemma(self,query):
        query=urlencode({"prompt":query})
        api=requests.get(f"https://mrapiweb.ir/chatbot/newrouter.php?{query}").text
        try:
            return api
        except:
            raise AIError("No Answer Found From Gemma. Please Try Again!") from None

    def zzzcode(prompt,language="python",mode="normal"):
        try:
            query = urlencode({"question":prompt,"lang":language,"mode":mode})
            return requests.get(f"https://mrapiweb.ir/chatbot/zzzcode.php?{query}").text
        except:
            raise AIError("No Answer Found From Zzzcode. Please Try Again!") from None
