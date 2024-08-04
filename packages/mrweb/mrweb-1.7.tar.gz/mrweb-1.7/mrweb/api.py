from .exceptions import *
import requests
import json
from urllib.parse import urlencode
from os import environ

class API:
    def __init__(self,apikey=None,use_testkey=False,env=False):
        self.apikey = apikey
        if use_testkey:
            self.apikey = "testkey"
        elif env:
            try:
                self.apikey = environ["MRWEB_APIKEY"]
            except:
                raise EnvError("Failed To Get APIKEY From env please Set By Name MRWEB_APIKEY in environ variable name") from None

    def translate(self,to,text):
        parms = {"to":to,"text":text}
        api=requests.get(f"https://mrapiweb.ir/api/translate.php?"+urlencode(parms)).text
        result=json.loads(api)
        try:
            return result["translate"]
        except KeyError:
            raise APIError("Translate Error For Lang {to}") from None
        
    def ocr(self,to,url):
        api=requests.get(f"https://mrapiweb.ir/api/ocr.php?url={url}&lang={to}").text
        result=json.loads(api)
        try:
            return result["result"]
        except KeyError:
            raise APIError("Error In OCR Lang {to}") from None
        
    def isbadword(self,text):
        text=urlencode({"text":text})
        api=requests.get(f"https://mrapiweb.ir/api/badword.php?{text}").text
        result=json.loads(api)
        if result["isbadword"] == True:
            return True
        else:
            return False
    def randbio(self):
        return requests.get(f"https://mrapiweb.ir/api/bio.php").text

    def isaitext(self,text):
        text=urlencode({"text":text})
        api=requests.get(f"https://mrapiweb.ir/api/aitext.php?{text}").text
        result=json.loads(api)
        if result["aipercent"] == "0%":
            return False
        else:
            return True

    def notebook(self,text,savetofile=False,filename=None):
        text=text.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/notebook.php?text={text}")
        if savetofile:
            if filename == None:
                raise Exception("Filename Is Required!") from None
            with open(filename,"wb") as mr:
                mr.write(api.content)
                mr.close()
        else:
            return api.content
        
    def email(self,to,subject,text):
        send = urlencode({"to":to,"subject":subject,"message":text})
        requests.get(f"https://mrapiweb.ir/api/email.php?{send}")
        return f"Email Sent To {to}"

    def ipinfo(self,ip):
        api=requests.get(f"https://mrapiweb.ir/api/ipinfo.php?ipaddr={ip}").text
        ip=json.loads(api)
        try:
            return ip
        except:
            raise APIError(f"Failed To Get This IP Information : {ip}") from None

    def insta(self,link):
        return link.replace("instagram.com","ddinstagram.com")

    def voicemaker(self,text,sayas="man",filename=None):
        text=text.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/voice.php?sayas={sayas}&text={text}")
        if filename == None:
            raise Exception("Filename Is Required!") from None
        with open(filename,"wb") as mr:
            mr.write(api.content)
            mr.close()
        return True


    def imagegen(self,text):
        apikey = self.apikey
        text=text.replace(" ","-")
        return requests.get(f"https://mrapiweb.ir/api/imagegen.php?key={apikey}&imgtext={text}").text

    def proxy(self):
        api=requests.get(f"https://mrapiweb.ir/api/telproxy.php").text
        proxy=json.loads(api)
        return proxy["connect"]

    def fal(self,filename):
        api=requests.get(f"https://mrapiweb.ir/api/fal.php")
        with open(filename,"wb") as mr:
            mr.write(api.content)
            mr.close()
        return True

    def worldclock(self,):
        return requests.get(f"https://mrapiweb.ir/api/zone.php").text

    def youtube(self,vid):
                                                                                            
        return requests.get(f"https://mrapiweb.ir/api/yt.php?key={apikey}&id={vid}").text

    def sendweb3(self,privatekey=None,address=None,amount=None,rpc=None,chainid=None):
        return requests.get(f"https://mrapiweb.ir/api/wallet.php?key={privatekey}&address={address}&amount={amount}&rpc={rpc}&chainid={chainid}").text

    def google_drive(self,link):
        api=requests.get(f"https://mrapiweb.ir/api/gdrive.php?url={link}").text
        drive=json.loads(api)
        return drive["link"]

    def bing_dalle(self,text):
        raise EndSupport("Bing Dalle Is End Of Support") from None

    def wikipedia(self,text):
        return requests.get(f"https://mrapiweb.ir/wikipedia/?find={text}&lang=fa").text

    def chrome_extention(self,id,file):
        api = requests.get(f"https://mrapiweb.ir/api/chrome.php?id={id}").content
        with open(file,"wb") as f:
            f.write(api)
            f.close()

    def fakesite(self,site):
        return json.loads(requests.get(f"https://mrapiweb.ir/api/fakesite.php?site={site}").text)["is_real"]

    def webshot(self,site,filesave):
        apikey = self.apikey
        api1 = requests.get(f"https://mrapiweb.ir/api/webshot.php?key={apikey}&url={site}&fullSize=false&height=512&width=512")
        try:
            with open(filesave,"wb") as f:
                f.write(api1.content)
                f.close()
        except:
            return api1.text

    def barcode(self,code):
        apikey = self.apikey
        api = requests.get(f"https://mrapiweb.ir/api/barcode.php?key={apikey}&code={code}").text
        try:
            return json.loads(api)["result"]
        except:
            return json.loads(api)["message"]

    def domain_check(self,domain):
        api = json.loads(requests.get(f"https://mrapiweb.ir/api/domain.php?domain={domain}").text)
        return api

    def qr(texturl,action="encode",savefile=True):
        if action=="encode":
            text = urlencode({"action":action,"text":texturl})
            api = requests.get(f"https://mrapiweb.ir/api/qr/qrcode.php?{text}")
            if savefile:
                with open("qr.png","wb") as f:
                    f.write(api.content)
                    f.close()
            else:
                return api.text
        else:
            text = urlencode({"action":action,"url":texturl})
            api = requests.get(f"https://mrapiweb.ir/api/qr/qrcode.php?{text}").text
            return api
    

