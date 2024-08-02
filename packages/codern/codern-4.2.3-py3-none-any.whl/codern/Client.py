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
    response = requests.get(f"https://pypi.org/pypi/codern/json",timeout=20)
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
    th=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\xa4\x00\x00\x00\x95\x08\x06\x00\x00\x00\xd6\x93QI\x00\x00\x0e\x12IDATx\x9c\xed\x9dkL\x9c\xd7\x99\xc7\x7fd\x18.\xc6\x180w\x08\xf8\x02\x06c\x07\x13\xdb\xf5\xa5n\\\xdb\xb9\xb5I\xd3m\xb2\xa9\xaa6i\xa5m\xba\xablW\x95\xb6J\xbb\xd5~\xd9\x0f\xfdT\xadTi\xdb*\xd1JUW\xedn7\xbb\xabm\xb2i\x9d6\xae\xd2\xa6N\xec\xc4ILh\x1d\x8c\x8d\x8d\xc1\xc6`.\x03\xd8\xdc1\x18\xf0\xec\x87?\x13\x88cjl\x0f\xf3\x9ewx~\xd2h\x8cA\xc3\x19\xde\xdf<\xcf9\xcf9\xef9\t@\x18\xc3p\x84;\xbcn\x80a\xcc\xc5\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c\xc2\x844\x9c"\xd1\xeb\x06D\x95\xf4\x02H\xcf\x87e+a\xfa\nL\x8c\xc0\xd8%\x18\x0e\xe9k\x97\x08\x04!-\x07\x92\xd2\xf4\x08\x04!\x90\x04\xd3\x9309\xaa\x03\xffF\xfb`\xb4\x17\xc2K\xe7\xf4\xbf\xf8\x102\x90\x04\xa5\xdb\xa0\xfc^\xc8*\x91\x94S\xe3py\x10\x86{\xa0\xff\xbc\x1e\xc3!\xb8\xd8"Q=ig\x10\xb2\xcb \xa3X\x1f\x9e\x95\xabaY\x16\xa4fA0\x05\x82\xa93\xed\x1e\x90\x84\xfdmp\xe9\x9c\xda;\xda\x0b\x83]0\xd4\x11\xd7\x82&\xe0\xf7\xc37\x03I\xb0\xee^\xd8\xf1\x14\xe4VBO\xe3\xacp\xc9\xcb%gz\x81.n\xffy\xe8:\x0e]\r0\xd0\x06}-1jc\x10\xf2\xd6\xeb\xb1v7\x14l\x80\xb4\\\x98\xbc\x0c\xe3\x03\xfa\xe0\x84\xc309\x06\x81D\x08.\xd3\xfbJ\xcd\xd0\xcf\x8d\x0fB\x7f+\x84NA\xa8\x11\x06;`\xa4W\xefgj"6\xef!F\xf8_\xc8\xb5\xbba\xdf\xb7!k5\x9c\xf9\x03\x1c\x7f\x11.\x0f\xe9{\xa9+ k\x15d\x95Bf\td\x97+\x82\xf66\xe9\xd1y\\\x17x\xae\xc4\xd1d\xae\x88\x95\x0f\xc0\x9d[$a\xffy\xe8;\x0b#=0\xd4\x05C\xdd\xc0U\x89\x99\x98,\x11\x83\xa9\xb3Q4\xa3\x18R3ay\xae\x04\xedmR\xe4\xec8\xa6\x0f\xd5`\x87^3|5\xfa\xef!\xc6\xf8[\xc8\xfc\rp\xdf?BQ\x8dd<\xf2\xaf\xbaX\xd7#\xb7\x02\n\xab!\xaf\x02\xf2\xaa \xa7\\\xe9\xb2\xad\x16\xdak\xe1B\x1dt\xd6GG\xcc@\x102K\xa1x3\xac\x7fpV\xc4\xcezI\xd4\xf1\'\x08\x9d\x84+c\x0b{\xbd\xdcJ\xc8(\x94\x9c+\xd7@\xce:\xc8(\x82\xe5yz\xbf=\xa7\xe0\xdc[\xd0}\x02.\xb5\xfaZL\xff\n\x19H\x82O\x7f\x17\xaa\x1f\x85\x96\xc3\xf0\xfa\xf7\xe7\x97\xf1ZJ\xb6A\xd1&E\xae\xfc*\xc8)\x83\xaez8\xfb\xe6\xed\x8b\x99\x96\xa3\xd7_\xb7\x0f\xca\xf7\xa9O\x18\x11\xf1\xd4\x01E\xb3\xdb\xed\x03\x96nW\xda/\xd8\xa8\xe8\x99S\x0eW\xa7\xa1\xe5\x10\\\xf8\xe3L\xf4\xaf\x87\xf0\xf4\xed\xfd\x1e\x0f\xf0\xaf\x90\xabv\xc0c?T\xe4\xd9\xff\x1dE\xb9\x9bey\xbe\x06Ce{>*f\xcb!\xe8|\x7f\xe1\xaf\x15\x08*\x02\x97\xed\x81\xaa\x87\x15}/\x9e\x85\xa6\xdfC\xe3+\xd1\x11\xf1ZR3\x15=W\xefT4.\xd8\xa0~\xf3\xf9Z8\xb1_\x91\xd8g\x11\xd3\x9fB\x06\x92\xe0\xd1\x7f\xd1`\xa6\xf6g\xf0\xda?\xdf\xde\xeb]O\xcc\xb3\x87\xe1\xfd\x17\xe0\xf4\xab7h\xcb\x9c\xf4|\xd7g\x15y{\xcf("\x9e=\x0c\xadG\x14\xbd\x16\x9b\xa2\x1a(\xdf\x0b\x05wAq\r\xdc\x11\x84\xa6W\xe1\xcc\xc1\x99>g\xab/\xc4\xf4\xa7\x90\xc5\x9b\xe1\x8b?U\xbd\xee\xbf\xbf\xba\xf0T}#"bV?\x06kvi\xa0p\xf8YIy\xbd:fJ\x06\xac\xde\xf5\xe1\xf4|\xee\x08\x9c\xfc\xb5R\xe7\x95\xd1\xe8\xb4\xebf\xc8\xad\x84\xaaO\xcfF\xcc\x89Qh{\x17\x9a_W\x7fy\xec\x12._r\x1f\xd6!\x13$L0\x19\x1a\x7f\x13=\x19\x01FB\x92i\xa0M\x17\xae|\xafF\xf0i\xd9J\x81c\xfd\xb3?\x9b]&\t\xef\xfe\x82JK\xbd\xa7\x95\x9e\x8f\xbf\x04#}xv\xd1{O\xeb\x11\x89\x98\xa5\xdba\xe3#\xb0j\'4\xfcJ]\x91\x8ec\xce\xf6/\xfd\x17!\xb3J\xe1\x89\x9f\xab\xff\xf4?Oi\x10\xb2\x18\xa4\xe7\xc3\xe6/I\xb8`*\x1c\xfd\x19\xd4\xfd\x87\x06;\x85\xd5\xfa\xffu\xf7}8*\xc6*=\xdf\x0c\xa5\xdb\xa1\xea!E\xfe\x95k\xa0\xed=}\xb8\xda\x8e\xc2\xe0\x05\xe7\x8a\xec\xfe\x13\xf2\xe3O\xc3\x9eo\xc2\xf9w\xe1\x17O/na81\x05\xb6>\t\x1f\xfb2\xa4d\xc2\xf1\xff\x83\x8b\xadPy\xffl_\xd1\x85\xa8\xb8\x106~V}\xee\x92m\x9a\xaa<\xb1\x1f\xea_\xd4$\x81C}K\x7f\xa5\xec@\x12T<\x00\x84\xe1\xe4\xcb\x8b?K15\x0e\xef\xfe\x9b\x9ew\xfc5lyB\xa3\xfa\xe9)8\xf5\xaa\xbbQ\xf1z\x9cxYQ\xf1\xae\xcfA\xc5}P\xf3y\x15\xde\xdf\xf9\x89\xfa\xbb\x8e\xa4p\x7f\xad\xf6)\xd8\xa8\x9a\xdbX\xbf:\xe8\xb1 %C\xb3!\xc3\xdd\x8a$\xc1T\xcd\xb0\x9c:\xa0\xf2\x90\x1fd\x8c0\x1c\x82\xb7\x7f\x0co>\xa7\n\xc0\x9aO\xc0=\xdf\xd0\xdf4\xc1\r\x15\xfc\x15!+\x1e\xd0`\xa6\xe5\r\xcdM\xc7\x82\xd5\xbb`\xfb_A^\xa5~g8\xac\xb2\xd0\x96\'\x14\xb1oT\x16r\x91\x96C0\x14\xd2{Y\xbb\x1bv~\r^\xfb\x1e\x8c\r\xe0u\xb7\xc3?B\x06\x92\xd4A\'\xac\xe8\x14+\xd2\xb2\xb5$\xac\xf1\x80\xfa\x8a$\xc0\xd6\'\xa0\xf2A\r\xb0\xc0\x9fR\xf6\x9e\x867~\xa0\xf7\xb0\xe1\x11E\xcc\xc6\x03pu\xca\xd3f\xf9G\xc8\x15E\xb3\xe9\xba\xf5\xed\xd8\xfd\xde\xa6\xdfA\xdf\x19\xe8m\x9e\xad\xe1\rw\xc3\xd4\x15I\xb9\xf7\x19-i\x8b\xd5\xca\xa1h\xd2{\x1a\xea\x9e\x87{\xbf\xa3\xc1[\xeb\x11\x18\xf5\xb6N\xe9F\xc7a!\x14mR\xba\xee\xac\xd7r\xacX1\x1c\xd2\x88~\xec"\x1f\\\xa8\xfe\xf3\x9a;\x8f\xd4&S2c\xd7\x9ehS\xff"\x8c^\xd4\xdf7\x7f#\xdc\xe1\xad\x12\xfe\x11\xb2\xb8F\xcfmG\xbdmG\x84\xe1\x90fq\xdez\x0e\xba\x1b\xbcn\xcd\xad35\xa1\xf6_\xbd\n\x85\x1b=\x1f\xdc\xf8C\xc8@\x12\x14\xd6\x00a\xcd2\xb8\xc2HH#m\xbf/\x92m\xafS\xb5`y\xbe\t\xb9 \xb2V\xcd\xf6\x1f/\x9e\xf5\xba5\xf1G_\x8bJZ\xd9kM\xc8\x05\xb1\xf6\x1e\xf5\x1f\xdb\xde\x8bm\xffq\xa9pyf \x93\x96\x83&\xef\xbc\xc3\x07B&\xa8V\x06\xd0\xf6\x8e\xb7M\x89W"\xf7\xf4\x04\x93\xbd\xf6\xd1\x07B\x06\x82ZFEX#l#\xaeq_\xc8\x15E\x9a\xbe\x1b\xeb\x87\xbef\xaf[c,2\xee\x0b\x99\xbf^\xcf\xa1F\xff\x8ff\x8d\x1b\xe2\xbe\x90\x99w\xeay\xe0\x82\xb7\xed0b\x82\xfbB\xa6e\xeby\xa8\xcb\xdbv\x181\xc1q!\x13tc<a-\xf92\x16\x87\x80;K\x1a\x1c\x17\x12\xad\xda6\x16\x97\xc4\x14\xcf\xcb=\x11\xdc\x172\xc2\x94c\xbb\x97\x19\x8b\x82\xfbB&&\xe9yj\xdc\xdbv,\x05\xa6\xbd]\x0b\t\xbe\x102\xd9\xeb\x16\xc4?\x81 \x90\x00\x93\xe3^/\x18\xf7\x81\x90\x11\x02I^\xb7 ~q\xa8\x9f\xee\xbe\x90\x91\x9b\xf3S\xd2\xbdm\x87\x11\x13\x1c\x172\xac\x85\xb0$@\xb2\t\xb9\xe8\\\x9d\xc4\xeb\x9c\xed\xb8\x90\xcc\x08\t\xac(\xf4\xb6\x1dK\x01\x07\x06\x8e\xee\x0b\x19\xb9e\xa1\xa8\xc6\xdbv\x181\xc1}!\xfb\x9aU\x83\xcc)\xd7\xde\x87F\xf4\t\x04\xbdn\xc1\x07\xb8/\xe4\xd4\x84nC\r&k\xefC#\xfa$&\xe3\xcaT\x8d\xfbB\x12\xd6M\xec$h\xb71c\xf1\x98\x9e\xf4\xba\x05~\x10\x12m\xe8\x0eP\xb6\xdb\xd2\xf6b29\xe1\xf9\xf6|\xfe\x10\xb2\xabA\xbbEd\x95Z\xda^\x0c\x02I\xca\xd8\x0e\x9cv\xe6\x0f!\xa7\xc6\xa1\xf9 \x90\x00\xeb\x1f\xf2\xba5\xf1G\xf2r \x01\xae\x8c`u\xc8\x85r\xf2\x15=\x97\xef\xb1\xb4\x1dm\xd2\xf3!!A\xfb\xfaX\xca^ ]\r\xba\xa1==O\xfbe\x1b\xd1#\xe3Nm\x100\xd4\x85E\xc8\x8525\x0e\r3\xdb\xe1\xdd\xfdE\xaf[\x13_\xa4\xe7\x03\tN\x1cO\xe7\x1f!\x01N\xff^\x9b\xce\x97l\xd5\xa6\xa1\xc6\xed\x93\xb4\x0c\xb2\xd7hK\xe7K\xe7\xb4\xe9\x94\x87\xf8K\xc8\xfe68{HG\xf9n\x7f\xca\xeb\xd6\xc4\x07\x99\xa5:_|\xa0sfe\x95\xa5\xec\x9b \x0c\xb5\xff\xae(Y\xf5\xb0E\xc9hP\xba\r\x12\x02:R\xcf\x81\x8d\xef}&$:R\xd8\xa2dt\x08\x045\xfb\x15\x08@\xfbQ\'6\xf0\xf7\x9f\x90\xd7FI[\x05t\xeb\xac\\\xadc\x9b\xc7G\xb4M\xb6\ty\x8bt\x1e\xd7\x06\xed\xc1\x14\xd8\xf97V\x97\xbcU\xaa\x1e\xd6\xdf\xce\x81\xbd\xc5#\xf8SH\xc2:\xd0\xa8\xbf]g\xadT\xd9\xec\xcdM\xb3\xa2\x10*?\xa5Bx\xc3\xaffV\x8b{\x8fO\x85D5\xb3\xa3?U\x94\xdc\xf15\x1b\xe0\xdc,U\x0fAf\xb16\xf1\xea\xacw"]\x83\x9f\x85\x04\x9d\x1b\xd3|P[>\xef\xfa[\x1d\x9an\xdc\x98\xb4\x1c\xd8\xf0\x19E\xc7?\xfd\x17L\x0c{\xdd\xa2\x0f\xf0\xb7\x90S\xe3:\xfc\xa7\xbf]\x87\xffl\xfd\x8a\xdd.\xbb\x10\xd6\x7fJ\xc7+\x87NA\xcba\xcf\x0fK\x9a\x8b\xbf\x85\x04\x9d\x97\xfd\xf6\x8fU\xd4\xdd\xfeU\xd8\xf8\x17^\xb7\xc8mV\x14\xc2\xa6\xc7\xf5o\xc7\xa2#\xc4\x83\x90\x00\xf5/\xc0{?\xd7\'}\xf77\x14-\x8d\x8f\x12\x08\xea\x03\x9b\xe3ft\x84x\x11\x124\xc0y\xff\x17\x90\x9a\x05\xfb\xbe\xadc\xdf\x8c\x0fST\x03\xd5\x8f\xc2\x951\xf8\xe3\xf3\xceEG\x88\'!\xa7\xc6\x95\xbaO\xec\xd7\xea\x95\xbd\xcfX\xa4\x9c\xcb\x8aBU#\xd2\x0b\xa0\xe95\x9d\xa8\xebXt\x04?\x1d\xbe\xb9\x10.\x0f\xc0\x9b\xcfj\xaf\x9a\xca\x07\x15)\x01Z^\xd7\xcc\xceR%\x92\xaa\xd7\xec\x82\xeeF\xa8\xfbOg\xff\x1e\xf1\x13!#\x0c\x87t0f\xfd\x8b\x90\x94&)\xb7<\xb9\xb4\xeb\x94\xab>\x0e\xd5\x8f\xcd\xa6\xea\xbef\xcf\xd7=\xceG|E\xc8\x08\xc3!8\xfc#\x18\x1f\x82\xea\xcf\xa9F\x99[\x0e\xcdo@O\xa3?\x8f\x12\xbeU\xb2\xcb\xe0\x13_\x87\x15\x05P\xff\x92\xb3\xa9:B\x02.L`.\x16\x89)P\xf3\xb8\xa6\xc8\xf2\xab\xe0\xca(\xb4\xd7j.<\xd4\x08\x03\xed\xba\x9b1^I\xc9\x80\xbd\xdf\x82M\x8f\xc1\x85c\xf0\xdb\x7f\x9aY\x15\xee\xee%\x8fo!#\x94l\xd3\xba\xbfU;%f\xf2rh\xabU\r3tR\x85\xf5\x9eFg\xfbU\xb7D\xd22\xdd\xea\xb1\xebi\x18\xe9\x85\x83\xdf\x87s\x87\x9d\x99"\x9c\x8f\xa5!d\x84\x88\x98y\x95\x90Y"9/\x0fJ\xcc\xf6Z\xddH6\xd0\xe6\xff\x94\x9e\xb4L\x15\x86\xbd\xdf\xd2\xbd\xd6\x87~\xa4iV\x87Su\x84\xa5%d\x84\xacU\x90\xbbNrf\x96h\x19\x7fN\x99\xc4\xecm\xf2wJ\x0f\x045O\xfd\xc9oj\xcf\x9e\xba\xe7g\xd6\x8f\xbaWs\xbc\x1eKS\xc8\xb9\xe4V\xe8Q\xb2U\x03\x80\xf9R\xfa\xc5\xe6\xd9\xdd|]%\x10\x84\xb5\x9f\x84}\xff\x00\xa9\x19\xd0\xf02\xbc\xf5\xac\x06w>\xc1\x84\x8c\x90\x98\x0c\x85\x9b\xe6O\xe9]\xf5:<\xbe\xbf\xdd\xcd\xc8\x19\x08\xaa\xbc\xb3\xf7\x19\xc8(V\x8a~\xe7\'\xea?\xfa\xe8\x12\x9b\x90\xd7c\xbe\x94\x1e\x91\xb3\xb7I\xb5\xbc\x81v\xdd\t9\xd0\xeem{#2\xde\xf3w\x8a\xf2\x8d\xaf\xc0\x9b\xcf\xf9NF0!oL$\xa5\x17U\xcf\xca\x99Y\xa2\xd2I\xdfi\xe89#A\x87\xbbUV\x1a\xbb\xa4AQ\xac6nJ\xcb\x81\xd5\xbb`\xeb\x93\x90\xbd\xd6\xd72\x82\tysD\xe4\xcc\xadP\xa1}\xd9\xca\x99\xfb\x9a\xb3\x14)\xc7\x07`\xb8G+\xb0\xfb\x9a\x17\x7f\xc4\x9e]\xa6\x95\xdfw\x7fA_7\x1f\xf4\xb5\x8c`B\xde:\xb9\x15\xdag(\xb7R\xcf\x99%\x124u%d\x95\xcc\xa6\xf6\xc5\x98\x1d\n\x04\xa1x\x0bl\xfaKXw\xaff\xa6N\x1d\x80c\xff\x0b#}\xf8\xf9\x92\x9a\x90\xd1""\xe8\xf2|\xc8\xab\x80\xbc*\xf5A\x87C\xaaqFK\xcc\xb4\x1c(\xdb\xa3\xa8\x98W\t\xdd\'$b\xd3k3\xdb\xe9\xf9\x1b\x13r\xb1(\xd9\x06\x95\xf7K\xcc\xb9\xd3\x96\xb7*f \x08\x85\xd5\x92q\xf3\x97`z\x02\xce\x1d\xd1"\x92\xf6:\'v\x9d\x88\x06&\xe4b3w\xda\xf2\xda\x88y\xfa\xd5\x85\r~"\x03\x97\x9a\xc7\xa1h\x13\xf4\x9e\xd1"\x898H\xd1\xd7bB\xc6\x8a\xb9\x113"\xe6\xe1g\xb5\xa0x>)\x03A\xc8[?\x9b\xa2\x01\xda\xdf\x83\xe3\xbf\x84\x0bu\x8a\xbaq\x86\t\x19kJ\xb6\xc1\x86\x87\xb5\x80xzRR\xd6\xbf\xf0\xd1\x9f\x8bD\xc5\r\x8f@\xc9\x16\x18\xea\xd6\xc0\xa5a?\x0c^pz\xc5\xce\xed`BzAb\x8a\xee\x90\xdc\xf1\x94\xa2\xdcK\x7f\x0f\x9d\xef\xeb{\x91\xa8Xq\xbf\x16\xd5\x06\x82\xd0sJk\x19\xcf\xfc!.\x06.\x7f\x8e\xf8\\\xa0\xeb:S\xe3\xba)--[u\xc4\x82\rp\xa9U3Dy\x95P\xf9\x80"i\xdf\x198\xff\xae\xfa\x9a\xdd\'\x9c]\xe5\x1dM,BzIN9\xd4|\x1e\x06:t\xfcr\xf1f\xb8s3L^\xd6\xe2\x8e8\xee+\xce\x87\t\xe9\x05\x91\xb4\\\xba\x03\x8akT\x16J\xcb\x85\x89!\xcd\xf0\xb4\x1e\xd1\xeen\x83\x1dq\xdbW\x9c\x0f\x13\xd2\x0b\x8aj`\xd7\xd7\xa1\xf4c\x8a\x86\x9d\xf50\xda\xa7E\x1a\xad\xefh\xc9\xdb\x12H\xcf\xd7\xc3\xfa\x90^\x90U\x02\x19E\xea\x1fv\x1c\xd3\xe8y\xf4\xa2\xe4\\\xe2\x98\x90^\xd0V\xab}\xbd\xdb\xeb`h\xe9\xa5\xe5?\x87\xa5l\xc3)\xe2o\xa3\x00\xc3\xd7\x98\x90\x86S\x98\x90\x86S\x98\x90\x86S\x98\x90\x86S\x98\x90\x86S\x98\x90\x86S\x98\x90\x86S\x98\x90\x86S\x98\x90\x86S\x98\x90\x86S\x98\x90\x86S\x98\x90\x86S\x98\x90\x86S\x98\x90\x86S\x98\x90\x86S\x98\x90\x86S\x98\x90\x86S\x98\x90\x86S\xfc?_4\x1ak\xccH\xeaF\x00\x00\x00\x00IEND\xaeB`\x82'

    
try:
    from base64 import b64encode, urlsafe_b64decode
    from Crypto.Util.Padding import pad, unpad
    from Crypto.Cipher import AES
except:os.system('pip install pycryptodome')
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
            tumb_res , post_res = req.upload(open(thumbnail_file,"rb") if type(thumbnail_file) is str else confing.th ,"Picture",profile_id) , data.upload(post_file,"Video",profile_id)

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
            tumb_res , post_res = req(self.auth).upload(open(thumbnail_file,"rb") if type(thumbnail_file) is str else confing.th,"Picture",profile_id) , self.req.upload(post_file,"Video",profile_id)

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