try:
    import requests,urllib3,os,httpx
    from colorama import init, Fore, Style
except:
    import os
    os.system("pip install colorama && requests && urllib3")
import json
from typing import Literal
from time import sleep
try:
    from bs4 import BeautifulSoup
    from requests import get
    import random,requests,pkg_resources
except:os.system("pip install bs4")
try:installed_version = pkg_resources.get_distribution('codern').version
except pkg_resources.DistributionNotFound:
    print(f"Package codern is not installed.")
except Exception as e:
    print(f"Error while checking the installed version: {e}")
    #    return
try:
    #print('connect...')
    response = requests.post(f"https://pypi.org/pypi/codern/json",timeout=20)
    if response.status_code == 200:
        latest_version = response.json()['info']['version']
        if installed_version != latest_version:print(f"New version Library : {latest_version}\n\n{Fore.GREEN}pip install codern=={latest_version}")
except:print('E connect Try Restart Source')
#except Exception as e:print(f"Error while fetching the latest version: {e}")

def get_useragent():
    return random.choice(_useragent_list)
import urllib3
import json
from typing import Any, Dict
class confing():
    headers= {
        "User-Agent": "okhttp/3.12.1",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json; charset=UTF-8"
        }
    server = {
            "rubino": "https://rubino17.iranlms.ir",
            "messenger": "https://messengerg2c137.iranlms.ir"
        }
    android = {
        "app_name": "Main",
        "app_version": "3.7.3",
        "lang_code": "fa",
        "package": "app.rbmain.a",
        "platform": "Android",
        "store": "Myket",
        "temp_code": "34"
    }
    thumbnail = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01\x90\x00\x00\x01,\x08\x03\x00\x00\x00\xdai\x15\xf0\x00\x00\x00\x03sBIT\x08\x08\x08\xdb\xe1O\xe0\x00\x00\x00\x1bPLTE\x00\x00\x00\xff\xff\xff\x81\x81\x81\xed\xed\xed\xcd\xcd\xcdbbb...\xa0\xa0\xa0DDD\xbcB\xe4\x12\x00\x00\x00_zTXtRaw profile type APP1\x00\x00\x08\x99\xe3JO\xcdK-\xcaLV((\xcaO\xcb\xccI\xe5R\x00\x03c\x13.\x13K\x13K\xa3D\x03\x03\x03\x0b\x03\x0804006\x04\x92F@\xb69T(\xd1\x00\x05\x98\x98\x9b\xa5\x01\xa1\xb9Y\xb2\x99)\x88\xcf\x05\x00O\xba\x15h\x1b-\xd8\x8c\x00\x00\x04\x03IDATx\x9c\xed\xdc\xdbz\xaaH\x10\x80\xd1\xd0\xa2\xf0\xfeO<\x93\x08\xda\xdd\x14\x89h\xf1\xcd\\\xacu\xb7\x89\xe6\x82?\x1c\x1a\xcb\xfd\xf5\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0\xcb\xe6\xff\xcd/\xe1G\x19?\xff\x1dc\xf9\xfcw\xb0(\xc3\xc7E\xc6A\x90<e\xf8\xb4\xc88\x08\x92\xe8\xdf \xc3\xf4\xc9/\x98\x06A2}\x07\xf9\xa4\xc8w\x0fA\x12\xfd\x04y\xbf\xc8O\x0fA\x12\xdd\x83\x0c\xd7\xf7\xde}\x1d\x04I\xb6\x04y\xaf\xc8\xd2C\x90Dk\x90w\x8a\xac=\x04I\xf4\x082\x1c^n\xcf\x83 \xf9\x9eA.\xb7c\xef\xbc]\x049\xc13\xc8\xc1"U\x0fA\x12UA\x0e\x15\xa9{\x08\x92\xa8\x0e2\\^\x7f_\xddC\x90DM\x90\xd7\x1fk\x8d\x83 \xe7hN=/\x17i{\x1c\xbd\x1d\xe07\xb7\xe1x\x91\xb6\xc7\xa0G\xaak\xbbw_x\xac5\xb5\xefx\xf3\xb1\x0b{\x8e\x16\xd1\xe3l\xd3\xa1"\xc7^\xcd;\x8e\xfc\xcd\x1f?\xc3q\xdc\xf8r\x91\xaeG\xc2\x88\x04\x8d\xe5\x91\xe2\xabE\xe2\x1e\xc6\x80\xf2,c@\xddrd\xef\xd1\xef\xdc\xbejY\x80L\x16\x86y\xcar\x15\xe8\x8a\xc4k\xbd\xf8E\x93\x95z\xa2\xb2>\xf8\x88\xff\xf8\x1b\xf1at\xf5\xe8$Sy\\1\xae\x7f\x15\xe9{<\xdf&H\x9e\xf2\xfcS/]\x91\xfe\xa5]\x8f{\x85\xdb H\xaa\xd2\\\x0c\x1a\xdd-mw#V_z\x04\xc9S\x86\x17\x8b\x84=\x96\xa3F\x90<\xa5\xd9\xf7\xe3n\x91\xf8\'\xe3 H\xb2\xd2\xee\xe1\xee:\xf1x0\xd2\x1d;\xcb\xf5e\xad$H\x9e\xd2\xee\xfb\xfeNj)\xd2\xf7\xe8\xcep\x82\xe4)\xdd\xbe\x0f\x8b\xc4=\x9eo\x15$Ou\xaf\x1b.G\xbewvw?\xbc}\xa1 y\xcao;\xfa\xbeu\xb3\xe1\xe7e\xf5\xca^\x90<\xc1\\V\x7f@l\x0f\x99/sY\xa7i\xe7\xb2\xc2\xe5H+\xba\xd4\x08\x92\xa8Y`\\\x82m\xadh\xc1\xe2S\xaaT\x97\xbf\xf6\xf7_?7\x96\x95\xab=\xfb4\x8fD6\x96#\xa89\xa7\xe9\x91\xad\x1d\x95\x8b\x97#\xcd\xbeo\xaf1>\xbfM\xd7\xde\xd7\xde\xefj\xbb\x81\xc6\xbb\xdb\xee\xcbI\x15\xed\xe2~\xf5\xb1\xf3\x037X\xa7\x88NB\x9b"\xd1\xa1c,\xeb$\xd1e:\x1cQ\xbcE7e\xe4Y/\xc9\xd1rd\xda\xf6\x08o\x92\xcde%*\xebI\'Z\xea\x8d\xbfmy~\xean.+\xd1:\x97\x15\x9f\x8b\xc6\xee\xdf\xe1\x02\xc4\\V\xa6\xf2\xb8q\x8d\x16\x88\xeb\xb6\xf0\xaa\xb2\xf40\x97\x95\xea9\x97\x15\xde\xcf\xde\x8b\x84\x8f\x81\xabw\t\x92\xa7T\xe7\x9eh9\xf2\xf3\xb1Gt\x1f\\\x1fW\x82\xe4\xa9\xe7\xb2\xbaC\xe0\x91a\xfb\x89\xd4\xd0^y\x04\xc9\xb3\xcce-\xff\x8a.\xda%\xf8D\xea\xb1 4\x97\x95\xad\x9d\xcb\xda\x7f\xae\x1e/\x08\xcde\xa5+\xf1.n7\xeem7\x97\x95\xaf\x9b\xcb\xda{4\x12\x1e9\xe6\xb2N\xb0\x19\xae\n\xaf\x15\xe1\x82\xd0\\\xd6\x196sY\xd1\xdd\xd4\xee\x02D\x90t\xf5\xbe\xde[\x8e\xc4\x0b\x90j\x93 y\xea s\xb0m3(\xb7\xee|\x83r\xe7\x88\x82t\x97\x8cp\x01"\xc8I\xc2 \x7f\x8e\x01}\tr\x968\xc8^\x91ja"\xc89v\x82\xc4\x83Y\xf5\xf7@\x059Iu,\xd4A\xa2\xc1\xacf$\xae\n\xe2\x93\xf5Tc\x18$\x1a\xccj~>\xebq\x961\xdc\xe1{c@\xabY\x8f\xd3\x8ca\x90\xbeH7\xa28\xebq\x9e)\x0c\x12\x8e\x01=\xcc\xf1fRLa\x90\xba\xc8f\xc7\xcfz\x9ci\n\x83l\xc6\x80*\xb3\x1e\xa7\x9a\xc2 k\x91\xe0\xff \x9f\xf58\xd75\x0c\xd2\x8c\x015f\xdfD8\xd95\xfc\xea\xcdw\x91\xf0;R\xb3\x1eg\xbb\x86\xdfM\xbb\xee\x1c\t7=\xfe#W{\x1e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \xd5?\xe90\x13,\xb8pR\x1b\x00\x00\x00\x00IEND\xaeB`\x82'


from base64 import b64encode, urlsafe_b64decode
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

class cryption:

    def __init__(self, auth:str):
        self.key = bytearray(self.secret(auth), 'UTF-8')
        self.iv = bytearray.fromhex('0' * 32)

    def replaceCharAt(self, e, t, i):
        return e[0:t] + i + e[t + len(i):]

    def secret(self, e):
        t = e[0:8]
        i = e[8:16]
        n = e[16:24] + t + e[24:32] + i
        s = 0
        while s < len(n):
            e = n[s]
            if e >= '0' and e <= '9':
                t = chr((ord(e[0]) - ord('0') + 5) % 10 + ord('0'))
                n = self.replaceCharAt(n, s, t)
            else:
                t = chr((ord(e[0]) - ord('a') + 9) % 26 + ord('a'))
                n = self.replaceCharAt(n, s, t)
            s += 1
        return n

    def encrypt(self, text):
        return b64encode(
            AES.new(self.key, AES.MODE_CBC, self.iv)
            .encrypt(pad(text.encode('UTF-8'),AES.block_size))
        ).decode('UTF-8')


    def decrypt(self, text):
        return unpad(
            AES.new(self.key, AES.MODE_CBC, self.iv)
            .decrypt(urlsafe_b64decode(text.encode('UTF-8')))
            ,AES.block_size
        ).decode('UTF-8')
    
    
    def changeAuthType(self, auth_enc):
        lowercase = 'abcdefghijklmnopqrstuvwxyz'
        uppercase = 'abcdefghijklmnopqrstuvwxyz'.upper()
        digits = '0123456789'
        n = ''
        for s in auth_enc:
            if s in lowercase:
                n += chr(((32 - (ord(s) - 97)) % 26) + 97)
            elif s in uppercase:
                n += chr(((29- (ord(s) - 65)) % 26) + 65)
            elif s in digits:
                n += chr(((13 - (ord(s)- 48)) % 10) + 48)
            else:
                n += s
        return n
    
from requests.exceptions import HTTPError , ReadTimeout , ConnectionError
from requests.sessions import Session ; Session = Session()
from json import dumps,loads
from requests.exceptions import HTTPError , ReadTimeout , ConnectionError
from requests.sessions import Session ; Session = Session()
from json import dumps,loads

class req:

    def __init__(self,auth:str):
        self.auth = auth
        self.enc = cryption(auth)

    def send_request(self,data:dict,method:str,type_method:str="rubino"):

        if type_method == "rubino":

            data_json = {
                "api_version": "0",
                "auth": self.auth,
                "client":confing.android,
                "data": data,
                "method": method
            }
            
        elif type_method == "messenger":

            data_json = {
                "api_version": "5",
                "auth": self.auth,
                "data_enc": self.enc.encrypt(
                    dumps({
                        "method": method,
                        "input": data,
                        "client": confing.android
                    })
                )
            }

        while True:
            try:
                response = Session.post(
                    url=confing.server[type_method],
                    headers=confing.headers,
                    json=data_json
                )
            except HTTPError as err:
                raise HTTPError(f"HTTP Error {err.args[0]}")
            except ReadTimeout:
                raise ReadTimeout('Time out')
            except ConnectionError:
                raise ConnectionError('Check your internet connection')
            except:
                continue
            else:
                if 'data_enc' in  response.json():
                    return loads(self.enc.decrypt(response.json()['data_enc']))
                return response.json()
        
    def requestUploadFile(self,file_name:str,size:str,file_type:str,profile_id:str=None):
        return self.send_request({
            "file_name": file_name,
            "file_size": str(size), 
            "file_type": file_type,
            "profile_id": profile_id
        },"requestUploadFile")

    def upload(self,post_file:str,post_type:str,profile_id:str=None):
        file_byte_code = post_file if type(post_file) is bytes else open(post_file,"rb").read()
        upload_res = self.requestUploadFile("video.mp4" if post_type == "Video" else "picture.jpg",len(file_byte_code),post_type,profile_id)
        if upload_res != None and upload_res["status"] == "OK":
            upload_res = upload_res["data"]
            total_part = len(file_byte_code) // 131072
            upload_data = 0
            for part in range(1, total_part + 2):
                beyte_part = file_byte_code[131072 * (part - 1) : 131072 * part]
                header={
                    "part-number":str(part),
                    "total-part":str(total_part + 1),
                    "auth":self.auth,
                    "hash-file-request":upload_res["hash_file_request"],
                    "file-id":str(upload_res["file_id"]),
                    "content-type": "application/octet-stream",
                    "content-length": str(len(beyte_part)),
                    "Host":upload_res["server_url"].replace("https://","").replace("/UploadFile.ashx",""),
                    "Connection":"Keep-Alive",
                    "accept-encoding": "gzip",
                    "user-agent": "okhttp/3.12.1",
                }
                while True:
                    try:
                        response = Session.post(data=beyte_part,url=upload_res["server_url"],headers=header)
                        if response.status_code == 200:
                            upload_data += round(len(beyte_part) / 1024)
                            print(f"\r{upload_data / 1000} MB | {round(len(file_byte_code) / 1024) / 1000} MB",end="\r")
                            break
                    except ConnectionError:
                        raise ConnectionError('Check your internet connection')
            return [upload_res, response.json()["data"]["hash_file_receive"]]
        return upload_res

class DateInfo:
    def __init__(self, data: Dict[str, Any]):
        self.jalali = data.get('jalali')
        self.miladi = data.get('miladi')
        self.ghamari = data.get('ghamari')

class SeasonInfo:
    def __init__(self, data: Dict[str, Any]):
        self.number = data.get('number')
        self.name = data.get('name')

class TimeInfo:
    def __init__(self, data: Dict[str, Any]):
        self.hour = data.get('hour')
        self.minute = data.get('minute')
        self.second = data.get('second')

class DayInfo:
    def __init__(self, data: Dict[str, Any]):
        self.number = data.get('number')
        self.name_week = data.get('name_week')
        self.name_month = data.get('name_month')

class MonthInfo:
    def __init__(self, data: Dict[str, Any]):
        self.number = data.get('number')
        self.name_past = data.get('name_past')
        self.name = data.get('name')

class YearInfo:
    def __init__(self, data: Dict[str, Any]):
        self.number = data.get('number')
        self.name = data.get('name')
        self.name_past = data.get('name_past')
        self.remaining = data.get('remaining')
        self.leap = data.get('leap')

class OccasionInfo:
    def __init__(self, data: Dict[str, Any]):
        self.miladi = data.get('miladi')
        self.jalali = data.get('jalali')
        self.ghamari = data.get('ghamari')

class TimeData:
    def __init__(self, data: Dict[str, Any]):
        self.timestamp = data.get('timestamp')
        self.date = DateInfo(data.get('date', {}))
        self.season = SeasonInfo(data.get('season', {}))
        self.time = TimeInfo(data.get('time', {}))
        self.day = DayInfo(data.get('day', {}))
        self.month = MonthInfo(data.get('month', {}))
        self.year = YearInfo(data.get('year', {}))
        self.occasion = OccasionInfo(data.get('occasion', {}))

    def __repr__(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False, indent=4, default=lambda o: o.__dict__)

class IPInfo:
    def __init__(self, data: Dict[str, Any]):
        self.ip = data.get('IP')
        self.country = data.get('Country')
        self.city = data.get('City')
        self.isp = data.get('ISP')
        self.timezone = data.get('timzone')
        self.org = data.get('org')
        self.country_code = data.get('countryCode')

    def __repr__(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False, indent=4)

def __request_url():
    import random
    return f"https://rubino{random.randint(1,59)}.iranlms.ir/"
from typing import Union, Optional
from pathlib import Path

_useragent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
]


def _req(term, results, lang, start, proxies, timeout):
    resp = get(
        url="https://www.google.com/search",
        headers={
            "User-Agent": get_useragent()
        },
        params={
            "q": term,
            "num": results + 2,  # Prevents multiple requests
            "hl": lang,
            "start": start,
        },
        proxies=proxies,
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp


class SearchResult:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"


def search(term, num_results=10, lang="en", proxy=None, advanced=False, sleep_interval=0, timeout=5):
    """Search the Google search engine"""

    escaped_term = term.replace(" ", "+")

    # Proxy
    proxies = None
    if proxy:
        if proxy.startswith("https"):
            proxies = {"https": proxy}
        else:
            proxies = {"http": proxy}

    # Fetch
    start = 0
    while start < num_results:
        # Send request
        resp = _req(escaped_term, num_results - start,
                    lang, start, proxies, timeout)

        # Parse
        soup = BeautifulSoup(resp.text, "html.parser")
        result_block = soup.find_all("div", attrs={"class": "g"})
        for result in result_block:
            # Find link, title, description
            link = result.find("a", href=True)
            title = result.find("h3")
            description_box = result.find(
                "div", {"style": "-webkit-line-clamp:2"})
            if description_box:
                description = description_box.text
                if link and title and description:
                    start += 1
                    if advanced:
                        yield SearchResult(link["href"], title.text, description)
                    else:
                        yield link["href"]
        sleep(sleep_interval)
import httpx
def get_mp3_links_with_title(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Unable to access {url}")
        return {}
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else 'No Title'
    links = soup.find_all('a')
    mp3_links = [link.get('href') for link in links if link.get('href') and link.get('href').endswith('.mp3')]
    if not mp3_links==[]:
        try:
            return {
        'name': title,
        'url': mp3_links[0]}
        except:...

class Email:
    def __init__(
            self,
            To: str,
            text: str,
            Title: str,
            Token: str,
            Input: Literal['info', 'app', 'Login', 'support'] = 'info'
        ) -> None:
        self.To = To
        self.text = text
        self.Title = Title
        self.Input = Input
        self.Token = Token
    
    def Send(self):
        Data = {
            'email': self.To,
            'text': str(self.text),  # تبدیل به رشته اطمینان می‌دهد که همیشه رشته است
            'head': self.Title,
            'token': self.Token,
            'title': self.Input
        }
        
        url = 'https://api-free.ir/api2/email.php'
        response = requests.post(url, data=Data)
        pars = response.json()
        print(pars)
        
        if pars.get('ok', False):
            return {
                'state': 'ok',
                'code': 200
            }
        else:
            return False

class client():
    def __init__(self,token: None = None,welcom: None = True)-> None:
        self.token=token
        self.welcom=welcom
        if welcom:
            message = f"""\n
            {Style.BRIGHT}Welcome to our library codern 3.8.16 !
            {Fore.GREEN}Website Dev : {Fore.RED}api-free.ir"""
            print(message)
    def Upload_file(self,Path)-> any:
        req=requests.post(
            "https://api-free.ir/api2/upload.php",
            data={'token':self.token},
            files={"file":open(Path,'rb')},
            timeout=60
        ).json()['result']
        return req
class api():
    def __init__(self,welcom : bool = True) -> None:
        """- view welcom dialog = bool : True"""
        self.welcom=welcom
        if welcom:print(f'{Style.BRIGHT}Welcome to our library codern')
    def __requests_data(methode:dict,parametr:dict):
        ...
    def search_music(text:str,result_count:None = 5):
        meta=search(text, num_results=result_count)
        meta=[result for result in meta]
        return [get_mp3_links_with_title(data) for data in meta]
    def create_voice(
            text:str,
            mod:Literal['FaridNeural', 'DilaraNeural'] = 'FaridNeural'
        ) -> None:
        request=urllib3.PoolManager()
        headers = {'Content-Type': 'application/json'}
        data={'text':text,'mod':mod}
        response=httpx.post(
            'https://api-free.ir/api/voice.php',
            data={'text':text,'mod':mod},
            timeout=60
        )
        if response.status_code == 200:
            response_data = response.json()
            if 'result' in response_data:
                return response_data['result']
    def create_image(
            text:str,
            version:Literal['3.5', '2.5','1.5','4'] = '3.5',
            choice : None = False):
            body = {'text': text,'v': version}
            request = urllib3.PoolManager()
            response = request.request(
            'POST',
            'https://api-free.ir/api/img.php',
            fields=body)
            if response.status == 200:
                response_data = json.loads(response.data.decode('utf-8'))
                if 'result' in response_data:
                    if not choice:
                        return response_data['result']
                    else : 
                        return random.choice(response_data['result'])
                
    def download_post_rubika(
            share_url:str,
            #return_choice:None = False
    ):
        body = {'url': share_url}
        request = urllib3.PoolManager()
        response = request.request(
            'POST',
            'https://api-free.ir/api/rubino-dl.php',
            fields=body)
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'result' in response_data:
                    return response_data['result']
            
    def download_story_rubika(
            username:str
    ):
        body = {'id': username}
        request = urllib3.PoolManager()
        response = request.request(
            'POST',
            'https://api-free.ir/api2/story_rubino.php',
            fields=body)
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'result' in response_data:
                    return response_data['result']
    def search_page_rubino(
            text:str
    ):
        body = {'user': text}
        request = urllib3.PoolManager()
        response = request.request(
            'GET',
            'https://api-free.ir/api/rubino-search.php',
            fields=body)
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'result' in response_data:
                    return response_data['result']
    def get_ip_me()->None:
        request = urllib3.PoolManager()
        response = request.request('GET','https://api-free.ir/api/ip.php')
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'ip' in response_data:
                    return response_data['ip']
    def get_info_ip(
            ip:str = None,

    )-> IPInfo:
        request = urllib3.PoolManager()
        if ip:body = {'ip':ip}
        else:body={'ip':''}
        #اگر مقدار ip وارد نشود آیپی کاربر را دریافت کرده و آیپی خود کاربر را اطلاعات میگیرد
        response = request.request('GET', 'https://api-free.ir/api/ips.php',fields=body)
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
        if 'result' in response_data:
            return IPInfo(response_data['result'])
        else:
            raise Exception("Failed to fetch time data from API.")
    def get_page_instagram(username):
        body = {'name': username}
        request = urllib3.PoolManager()
        response = request.request(
            'GET',
            'https://api-free.ir/api/insta.php',
            fields=body)
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'Result' in response_data:
                    return response_data['Result']
    def search_wikipedia(
            text:str,
            lang:None = "fa"
    ):
        body = {'text': text,'lang':lang}
        request = urllib3.PoolManager()
        response = request.request(
            'POST',
            'https://api-free.ir/api/wiki.php',
            fields=body)
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'result' in response_data:
                    return response_data['result']
    def Ai_chat_GPT(text:str)->None:
        body = {'text': text}
        request = urllib3.PoolManager()
        response = request.request(
            'POST',
            'https://api-free.ir/api/chat.php',
            fields=body)
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'result' in response_data:
                    return response_data['result']
    def Ai_bard_Chat(
              text:str,
              put_lang:Literal['fa','en']='fa'):
        body = {'text': text}
        request = urllib3.PoolManager()
        response = request.request(
            'POST',
            'https://api-free.ir/api/bard.php',
            fields=body)
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'result' in response_data:
                    if put_lang=="fa":return response_data['result']
                    elif put_lang=="en":return response_data['result_en']
                    else:raise KeyboardInterrupt("error Input Lang : { fa or en }")
    def Ai_black_box(text: str,is_replace: str = None,*args, **kwargs) -> dict:
        if is_replace:
            text=text.replace(is_replace,'')
        body = {'text': text}
        request = urllib3.PoolManager()
        response = request.request(
            'GET',
            'https://api-free.ir/api/black-box',
            fields=body)
        if response.status == 200:
            #print(response.data.decode('utf-8'))
            return response.data.decode('utf-8')
    def add_Tag_img(
            text:Optional[str],
            Input_name_file: Union[Path, bytes],
            save_as:Optional[str],
            size_text: Optional[int] = 30,
        ):
        s=requests.post(
            'https://uploadkon.ir/',
            data={
                'ajax':1,
                'submitr':1
            },
            files={
                'file':open(
                    Input_name_file,"rb"
                )
            })
        pars=s.json()[0]['i']
        jpg_urls = __import__('re').findall(r'https?://\S+?\.jpg', pars)[0]
        response=requests.post(f"https://api.api-free.ir/Tag/?text={text}&url={jpg_urls}&size={size_text}")
        if response.status_code ==200:
            with open(save_as,'wb') as f:
                f.write(response.content)
                return {'ok':True}
        else:
             return {'ok':False}
    def create_captcha(
        text: str,
        font: Literal['1', '2', '3', '4', '5'] = '3',
        background: Literal['1', '2', '3', '4', '5'] = '1',
        *args,
        **kwargs
    ):
        if not (text.isdigit() and len(text) == 5):
            raise ValueError("Text must be a 5-digit number.")
        if font not in {'1', '2', '3', '4', '5'}:
            raise ValueError("Font must be a value between '1' and '5'.")
        if background not in {'1', '2', '3', '4', '5'}:
            raise ValueError("Background must be a value between '1' and '5'.")
        body = {
            'text': text,
            'font': font,
            'back': background
        }
        request = urllib3.PoolManager()
        response = request.request(
            'GET',
            'https://api-free.ir/api/CP.php',
            fields=body
        )
        if response.status == 200:
            response_data = json.loads(
                response.data.decode(
                    'utf-8'
                )
            )
            if 'result' in response_data:
                return response_data['result']
        else:
            raise Exception(
                "Failed to fetch captcha from API."
            )
    def get_time() -> TimeData:
        request = urllib3.PoolManager()
        response = request.request('GET', 'https://api-free.ir/api/time2.php')
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
        if 'result' in response_data:
            return TimeData(response_data['result'])
        else:
            raise Exception("Failed to fetch time data from API.")
    def translate(
        text:str,
        to:str
    ):
        body = {
            'text': text,
            'from':'auto',
            'to':to
        }
        request = urllib3.PoolManager()
        response = request.request(
            'GET',
            'https://api-free.ir/api/Trans.php',
            fields=body)
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'result' in response_data:
                    return response_data['result']
    def search_google(
            text:str,
            num_result = 5,
            lang='fa'
    ):
        from googledata import search
        data = search(
            term=text,
            num_results=num_result,
            lang=lang
        )
        return [m for m in data]
    def add_size_fake(file, save_as, size):
        import os
        size = os.path.getsize(file)
        with open(file, 'rb') as input_file:
            with open(save_as, 'wb') as khorogi:
                tekrar = size * 1024 * 1024 // size
                bytess = size * 1024 * 1024 % size
                for target in range(tekrar):
                    print(target)
                    input_file.seek(0)
                    khorogi.write(input_file.read())
                input_file.seek(0)
                khorogi.write(input_file.read(bytess))

class rubino():
    def __init__(self,auth) -> None:
        """- auth : شناسه اکانت وارد شود"""
        self.auth=auth
    def _request_url(self):
        import random
        return f"https://rubino{random.randint(1,59)}.iranlms.ir/"
    def get_link(self):
        return self._request_url()
    def _reuests_post(self,methode:str,data:dict):
        request = urllib3.PoolManager()
        body = {
            "auth":self.auth,
            "api_version":"0",
            "client":{
                "app_name":"Main",
                "app_version":"2.2.4",
                "package":"m.rubika.ir",
                "platform":"PWA"
            },
            "data":data,
            "method":methode
        }
        response = request.request(
            'POST',
            self.get_link(),
            json=body)
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'data' in response_data:
                    return response_data['data']
            else:
                return response_data['status_det']
        else :
            raise Exception("Request Error Server")
    def edit_info_page(
        self,
        username_me:str,
        name=str,
        bio=None,
        phone=None,
        email=None,
        website=None
        ):
        """
        - username_me : در این مقدر باید آیدی پیجی که میخاین ادیت شه وارد کنید
        """
        profile_id=requests.post(f"https://api-free.ir/api/rubino-search.php?user={username_me}").json()['result']['data']['profiles'][0]['id']
        data = {
            "profile_id":profile_id,
            "username":username_me,
            "name":name,
            "bio":bio,
            "phone":phone,
            "email":email,
            "website":website
        }
        methode = "updateProfile"
        req_get = self._reuests_post(methode=methode,data=data)
        return req_get
    def create_page(
            self,
            username:str,
            name:str = "codern",
            bio:str = None,
            phone=None,
            email=None,
            website=None
            ):
        data = {
            "username":username,
            "name":name,
            "bio":bio,
            "phone":phone,
            "email":email,
            "website":website
        }
        methode = "createPage"

        request = self._reuests_post(methode=methode,data=data)
        return request
    def Download_story(self,username):
        return api.download_story_rubika(username)
    def get_comments(self,post_id,post_profile_id,profile_id=None):
        data = {
            "equal": False,
            "limit": 100,
            "sort": "FromMax",
            "post_id": post_id,
            "profile_id": profile_id,
            "post_profile_id": post_profile_id
        }
        methode = "getComments"
        request = self._reuests_post(methode=methode,data=data)
        return request
    def get_all_profile(self):
        data = {"equal":False,"limit":10,"sort":"FromMax"}
        methode = 'getProfileList'
        request = self._reuests_post(methode=methode,data=data)
        return request
    def get_me_info(self,profile_id):
        """- دریافت اطلاعات پیج"""
        data = {"profile_id":profile_id}
        methode = 'getMyProfileInfo'
        request = self._reuests_post(methode=methode,data=data)
        return request
    def Like(self,post_id,target_post_id):
        data ={"action_type":"Like","post_id":post_id,"post_profile_id":target_post_id,"profile_id":[]}
        methode = 'likePostAction'
        request = self._reuests_post(methode=methode,data=data)
        return request
    
    #--------------------------------------------

    def comment(self,text,post_id,post_target_id,profile_id=None):
        data = {
            "content": text,
            "post_id": post_id,
            "post_profile_id": post_target_id,
            "rnd":f"{random.randint(100000,999999999)}" ,
            "profile_id":profile_id
        }
        methode = 'addComment'
        while True:
            try:return self._reuests_post(methode=methode,data=data)
            except:return "error"
    
    def get_link_share(self,post_id,post_profile,prof=None):
        data = {
            "post_id":post_id,
            "post_profile_id":post_profile,
            "profile_id":prof
        }
        methode = 'getShareLink'
        return self._reuests_post(methode=methode,data=data)
    
    
    def is_Exist_Username(self,username):
        if username.startswith("@"):
            username = username.split("@")[1]
            data = {"username": username}
        else:data = {"username": username}
        methode = "isExistUsername"
        return self._reuests_post(methode=methode,data=data)
    
    def add_View_Story(self,target_story_id,ids:list,profile_id=None):
        data = {
            "profile_id":profile_id,
            "story_ids":ids,
            "story_profile_id":target_story_id
        }
        methode = 'addViewStory'
        return self._reuests_post(methode=methode,data=data)
               

    def save_post(self,post_id,post_profile_id,prof=None):
        data = {
            "action_type":"Bookmark",
            "post_id":post_id,
            "post_profile_id":post_profile_id,
            "profile_id":prof
        }
        methode ='postBookmarkAction'
        return self._reuests_post(methode=methode,data=data)
               

    def un_like(self,post_id,post_profile_id):
        data = {
            "action_type":"Unlike",
            "post_id":post_id,
            "post_profile_id":post_profile_id,
            "profile_id":[]
        }
        methode ='likePostAction'
        return self._reuests_post(methode=methode,data=data)
    def get_Suggested(self,profile_id=None):
        data = {
            "profile_id":profile_id,
            "limit": 20,
            "sort": "FromMax"
        }
        methode = 'getSuggested'
        return self._reuests_post(methode=methode,data=data)
    def add_Post(self,post_file:str,caption:str=None,duration:int=27,size:list=[668,798],thumbnail_file:str=None,profile_id:str=None):
        if post_file.split(".")[-1] == "mp4" or post_file.split(".")[-1] == "mov" or post_file.split(".")[-1] == "mkv":
            tumb_res , post_res = req.upload(open(thumbnail_file,"rb") if type(thumbnail_file) is str else confing.thumbnail ,"Picture",profile_id) , data.upload(post_file,"Video",profile_id)

            data = {
                "caption": caption,
                "duration": str(duration),
                "file_id": post_res[0]["file_id"],
                "hash_file_receive": post_res[1],
                "height": "862" if size[1] > 862 else str(size[1]),
                "is_multi_file": False,
                "post_type": "Video",
                "rnd": random.randint(100000, 999999999),
                "snapshot_file_id": tumb_res[0]["file_id"],
                "snapshot_hash_file_receive": tumb_res[1],
                "tagged_profiles": [],
                "thumbnail_file_id": tumb_res[0]["file_id"],
                "thumbnail_hash_file_receive": tumb_res[1],
                "width": "848" if size[0] > 848 else str(size[0]),
                "profile_id": profile_id
            }

        elif post_file.split(".")[-1] == "jpg" or post_file.split(".")[-1] == "png":
            post_res = req(self.auth).upload(post_file=post_file,post_type="Picture",profile_id=profile_id)

            data = {
                "caption": caption,
                "file_id": post_res[0]["file_id"],
                "hash_file_receive": post_res[1],
                "height": "862" if size[1] > 862 else str(size[1]),
                "is_multi_file": False,
                "post_type": "Picture",
                "rnd": random.randint(100000, 999999999),
                "tagged_profiles": [],
                "thumbnail_file_id": post_res[0]["file_id"],
                "thumbnail_hash_file_receive": post_res[1],
                "width": "848" if size[0] > 848 else str(size[0]),
                "profile_id": profile_id
            }
        else:
            return "file address eror"
        return req(self.auth).send_request(data,"addPost")
    def get_Post_Likes(self,post_profile_id:str,post_id:str,max_id:str,sort:str="FromMax",limit:int=50,equal:bool=False,profile_id:str=None):
        data = {
            "equal": equal,
            "limit": limit,
            "max_id": max_id,
            "post_id": post_id,
            "post_profile_id": post_profile_id,
            "sort": sort,
            "profile_id": profile_id
        }
        return self._reuests_post(methode='getPostLikes',data=data)
    
    def get_Story(self,story_profile_id:str,story_ids:list,profile_id:str=None):
        return self._reuests_post(data={
            "profile_id": profile_id,
            "story_ids": story_ids,
            "story_profile_id": story_profile_id
        },methode="getStory")
    
    def get_Story_Viewers(self,story_id:str,limit:int=50,profile_id:str=None):
        return self._reuests_post(data={
            "limit": limit,
            "profile_id": profile_id,
            "story_id": story_id
        },methode="getStoryViewers")
    
    def get_My_Archive_Stories(self,sort:str="FromMax",limit:int=10,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "sort": sort,
            "profile_id": profile_id
        },methode="getMyArchiveStories")
    
    def get_Page_Highlights(self,target_profile_id:str,sort:str="FromMax",limit:int=10,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "sort": sort,
            "target_profile_id": target_profile_id,
            "profile_id": profile_id
        },methode="getProfileHighlights")
    
    def create_Highlight(self,highlight_name:str,story_ids:list,highlight_cover_picture:str,profile_id:str=None):
        highlight_cover_res = self.req.upload(highlight_cover_picture,"Picture",profile_id)
        return self._reuests_post(data={
            "highlight_cover": {
                "highlight_file_id": highlight_cover_res[0]["file_id"],
                "highlight_hash_file_receive": highlight_cover_res[1],
                "type": "File"
            },
            "highlight_name": highlight_name,
            "story_ids": story_ids,
            "profile_id": profile_id
        },methode="addHighlight")
    
    def highlight_Story(self,highlight_id:str,story_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "highlight_id": highlight_id,
            "story_id": story_id,
            "profile_id": profile_id
        },methode="highlightStory")
    
    def remove_Story_From_Highlight(self,highlight_id:str,remove_story_ids:list,profile_id:str=None):
        return self._reuests_post(data={
            "highlight_id": highlight_id,
            "remove_story_ids": remove_story_ids,
            "updated_parameters":["remove_story_ids"],
            "profile_id": profile_id
        },methode="editHighlight")
    
    def get_Hash_Tag_Trend(self,sort:str="FromMax",limit:int=50,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "sort": sort,
            "profile_id": profile_id
        },methode="getHashTagTrend")
    
    def get_Explore_Posts(self,sort:str="FromMax",limit:int=51,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "sort": sort,
            "profile_id": profile_id
        },methode="getExplorePosts")
    
    def get_Tagged_Posts(self,target_profile_id:str,sort:str="FromMax",limit:int=50,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "sort": sort,
            "target_profile_id": target_profile_id,
            "profile_id": profile_id
        },methode="getTaggedPosts")
    
    def delete_Comment(self,post_id:str,comment_id:str,text:str,profile_id:str=None):
        return self._reuests_post(data={
            "model": "Comment",
            "post_id": post_id,
            "record_id": comment_id,
            "profile_id": profile_id
        },methode="removeRecord")
    
    def like_Comment(self,comment_id:str,post_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "action_type": "Like",
            "comment_id": comment_id,
            "post_id": post_id,
            "profile_id": profile_id
        },methode="likeCommentAction")
    
    def un_like_Comment(self,comment_id:str,post_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "action_type": "Unlike",
            "comment_id": comment_id,
            "post_id": post_id,
            "profile_id": profile_id
        },methode="likeCommentAction")
    
    def get_Comments(self,post_profile_id:str,post_id:str,sort:str="FromMax",limit:int=50,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "post_id": post_id,
            "post_profile_id": post_profile_id,
            "sort": sort,
            "profile_id": profile_id
        },methode="getComments")
    
    def request_Follow(self,followee_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "f_type": "Follow",
            "followee_id": followee_id,
            "profile_id": profile_id
        },methode="requestFollow")
    
    def un_Follow(self,followee_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "f_type": "Unfollow",
            "followee_id": followee_id,
            "profile_id": profile_id
        },methode="requestFollow")
    
    def get_Page_Follower(self,target_profile_id:str,sort:str="FromMax",limit:int=50,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "f_type": "Follower",
            "limit": limit,
            "sort": sort,
            "target_profile_id": target_profile_id,
            "profile_id": profile_id
        },methode="getProfileFollowers")
    
    def get_Page_Following(self,target_profile_id:str,sort:str="FromMax",limit:int=50,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "f_type": "Following",
            "limit": limit,
            "sort": sort,
            "target_profile_id": target_profile_id,
            "profile_id": profile_id
        },methode="getProfileFollowers")
    
    def search_Follower(self,target_profile_id:str,username:str,max_id:str,sort:str="FromMax",limit:int=50,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "max_id": max_id,
            "search_type": "Follower",
            "sort": sort,
            "target_profile_id": target_profile_id,
            "username": username,
            "profile_id": profile_id
        },methode="getProfileFollowers")
    
    def search_Following(self,target_profile_id:str,username:str,max_id:str,sort:str="FromMax",limit:int=50,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "max_id": max_id,
            "search_type": "Following",
            "sort": sort,
            "target_profile_id": target_profile_id,
            "username": username,
            "profile_id": profile_id
        },methode="getProfileFollowers")
    
    def get_NewFollow_Requests(self,sort:str="FromMax",limit:int=50,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "sort": sort,
            "profile_id": profile_id
        },methode="getNewFollowRequests")
    
    def accept_Request_Follow(self,request_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "action": "Accept",
            "request_id": request_id,
            "profile_id": profile_id
        },methode="actionOnRequest")
    
    def decline_Request_Follow(self,request_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "action": "Decline",
            "request_id": request_id,
            "profile_id": profile_id
        },methode="actionOnRequest")
    def un_save_Post(self,post_profile_id:str,post_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "action_type": "Unbookmark",
            "post_id": post_id,
            "post_profile_id": post_profile_id,
            "track_id": "Related",
            "profile_id": profile_id
        },methode="postBookmarkAction")
    
    def get_Saved_Posts(self,sort:str="FromMax",limit:int=51,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "sort": sort,
            "profile_id": profile_id
        },methode="getBookmarkedPosts")
    
    def search_Page(self,username:str,sort:str="FromMax",limit:int=50,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "sort": sort,
            "username": username,
            "profile_id": profile_id
        },methode="searchProfile")
    
    def block_Page(self,target_profile_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "action": "Block",
            "blocked_id": target_profile_id,
            "profile_id": profile_id
        },methode="setBlockProfile")
    
    def un_block_Page(self,target_profile_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "action": "Unblock",
            "blocked_id": target_profile_id,
            "profile_id": profile_id
        },methode="setBlockProfile")
    
    def report_Page(self,post_id:str,reason:int=2,profile_id:str=None):
        # reason is 1 or 2 -> reason 1 = هرزنامه / reason 2 = نامناسب
        return self._reuests_post(data={
            "model": "Profile",
            "reason": reason,
            "record_id": post_id,
            "profile_id": profile_id
        },methode="setReportRecord")

    def delete_Post(self,post_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "model": "Post",
            "record_id": post_id,
            "profile_id": profile_id
        },methode="removeRecord")
    
    def delete_Story(self,story_id:list,profile_id:str=None):
        return self._reuests_post(data={
            "profile_id": profile_id,
            "story_id": story_id,
        },methode="deleteStory")
    
    def set_Page_Status(self,profile_status:str="Private",profile_id:str=None):
        # profile_status is Private or Public
        return self._reuests_post(data={
            "profile_status": profile_status,
            "profile_id": profile_id
        },methode="updateProfile")

    def allow_Send_MessagePv(self,is_message_allowed:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "is_message_allowed": is_message_allowed,
            "profile_id": profile_id
        },methode="updateProfile")
    
    def edit_Notification(self,is_mute:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "is_mute": is_mute,
            "profile_id": profile_id
        },methode="updateProfile")
    
    def upload_avatar(self,prof_file:str,profile_id:str=None):
        prof_res = req(self.auth).upload(prof_file,"Picture",profile_id)
        return self._reuests_post(data={
            "file_id": prof_res[0]["file_id"],
            "hash_file_receive": prof_res[1],
            "thumbnail_file_id": prof_res[0]["file_id"],
            "thumbnail_hash_file_receive": prof_res[1],
            "profile_id": profile_id
        },methode="updateProfilePhoto")
    def add_Story(self,post_file:str,duration:int=27,size:list=[668,798],thumbnail_file:str=None,profile_id:str=None):
        
        if post_file.split(".")[-1] == "mp4" or post_file.split(".")[-1] == "mov" or post_file.split(".")[-1] == "mkv":
            tumb_res , post_res = req(self.auth).upload(open(thumbnail_file,"rb") if type(thumbnail_file) is str else confing.thumbnail,"Picture",profile_id) , self.req.upload(post_file,"Video",profile_id)

            data = {
                "duration": str(duration),
                "file_id": post_res[0]["file_id"],
                "hash_file_receive": post_res[1],
                "height": 1280 if size[1] > 1280 else size[1],
                "story_type": "Video",
                "rnd": random.randint(100000, 999999999),
                "snapshot_file_id": tumb_res[0]["file_id"],
                "snapshot_hash_file_receive": tumb_res[1],
                "thumbnail_file_id": tumb_res[0]["file_id"],
                "thumbnail_hash_file_receive": tumb_res[1],
                "width": 720 if size[0] > 720 else size[0],
                "profile_id": profile_id
            }
                
        elif post_file.split(".")[-1] == "jpg" or post_file.split(".")[-1] == "png":
            post_res = req(self.auth).upload(post_file,"Picture",profile_id)

            data = {
                "file_id": post_res[0]["file_id"],
                "hash_file_receive": post_res[1],
                "height": 1280 if size[1] > 1280 else size[1],
                "story_type": "Picture",
                "rnd": random.randint(100000, 999999999),
                "thumbnail_file_id": post_res[0]["file_id"],
                "thumbnail_hash_file_receive": post_res[1],
                "width": 720 if size[0] > 720 else size[0],
                "profile_id": profile_id
            }
        else:
            return "file address eror"
        return req(self.auth).send_request(data,"addStory")['data']
    def delete_Page(self,page_profile_id:str):
        return self._reuests_post(data={
            "model": "Profile",
            "record_id": page_profile_id,
            "profile_id": None
        },methode="removeRecord")
    
    def add_Post_View_Count(self,post_profile_id:str,post_id:str):
        return self._reuests_post(data={
            "post_id": post_id,
            "post_profile_id": post_profile_id
        },methode="addPostViewCount")

    def add_Post_View_Time(self,post_profile_id:str,post_id:str,duration:int,profile_id:str=None):
        return self._reuests_post(data={
            "duration": duration,
            "post_id": post_id,
            "post_profile_id": post_profile_id,
            "profile_id": profile_id
        },methode="addPostViewTime")['data']