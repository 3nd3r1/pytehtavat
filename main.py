from bs4 import BeautifulSoup
import requests

s = requests.Session()

def getUserCookies():
    cookies = {
    'dancer.session':'521062877299624071118135967688004881',
    'lang':'fi',
    '_ga':'GA1.2.508072976.1544784292',
    '_gid':'GA1.2.1900992478.1544784292',
    '__zlcmid':'prhrg7Wt3yrruR'
    }  
    tiedot = {
    'username':'LTI8HCaHcZ',
    'password':'-',
    'path':'',
    'lang':'',
    'org_short':'',
    'auth_method':''
    }
    return cookies,tiedot
cookies,tiedot = getUserCookies()
s.post("http://vw4.viope.com/login", data=tiedot)
r = s.get("https://vw4.viope.com/student/6314/#/content")



print(r.cookies)
