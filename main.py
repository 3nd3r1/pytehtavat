from selenium import webdriver
from bs4 import BeautifulSoup
import time

def SanomaProLogin():
    url = "https://kirjautuminen.sanomapro.fi/sso/XUI/#login/&realm=%2Fratkoo"
    username = "-"
    password = "-"

    d = webdriver.Chrome("chromedriver.exe")

    #Wait because the page has a load.
    d.get(url)
    d.implicitly_wait(5)
    
    d.find_element_by_id("username").send_keys(username)
    d.find_element_by_id("password").send_keys(password)
    d.find_element_by_id("loginButton_0").click()
    d.implicitly_wait(5)

    d.get("https://oppimisymparisto.sanomapro.fi/d2l/le/content/custom/1545693/57176258/Viewer")
    d.implicitly_wait(5)
    d.get("https://vw4.viope.com/student/6314/#/content")
    
    d.implicitly_wait(5)
    time.sleep(5)
    bs = BeautifulSoup(d.page_source,"html.parser")
    for x in bs.find_all("span",{"class":"test-exe"}):
        print(x.text)
    
SanomaProLogin()

