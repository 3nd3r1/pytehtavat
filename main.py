from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time

    
def SanomaProLogin(username, password):
    while (True):
        try:
            url = "https://kirjautuminen.sanomapro.fi/sso/XUI/#login/&realm=%2Fratkoo"

            d = webdriver.Chrome("chromedriver.exe")

            d.get(url)
            d.implicitly_wait(10)
    
            d.find_element_by_id("username").send_keys(username)
            d.find_element_by_id("password").send_keys(password)
            d.find_element_by_id("loginButton_0").click()
            d.implicitly_wait(10)

            d.get("https://oppimisymparisto.sanomapro.fi/d2l/le/content/custom/1545693/57176258/Viewer")
            d.implicitly_wait(10)
        except:
            continue
        break

    return d

def saveAnswers(username, password):
    
    d = SanomaProLogin(username,password)
    d.get("https://vw4.viope.com/student/6314/#/content")

    time.sleep(1)
    bs = BeautifulSoup(d.page_source,"html.parser")



    #Get 4 divs and use the second
    
    divit = []
    for x in bs.find_all("div",{"class":"course_expanded"}):
        for y in x.find_all("div",{"ng-repeat":"type in ex_types","class":"ng-scope"}):
            divit.append(y)
    with open("answers.txt","a") as fp:
        
        for y in range(1,len(divit),4):
            for x in divit[y].find_all("span",{"class":"test-exe"}):
                if("Random" in x["title"].split(".")[0]):
                    vips = 4
                else:
                    vips = x["title"].split(".")[0]
                kakat = d.find_elements_by_class_name("btn-course")
                kakat[int(vips)-1].click()
                d.implicitly_wait(10)

                print(x['title'])
                fp.write(x["title"])
                fp.write("\n")
                exa = '//span[@title="'+x["title"]+'"]'
                element = WebDriverWait(d, 10).until(
                EC.element_to_be_clickable((By.XPATH, exa))
                )
                element.click()
                
                exa = '//button[@ng-click="showExampleAnswer()"]'
                element = WebDriverWait(d, 10).until(
                EC.element_to_be_clickable((By.XPATH, exa))
                )
                element.click()

                jatka = True
                while (jatka):
                    asd = BeautifulSoup(d.page_source,"html.parser")
                    for a in asd.find_all("div",{"class":"prog-example-answer"}):
                        ribs = a.find_all("pre")
                        for b in range(1,len(ribs)):
                            fp.write(ribs[b].text)
                            if(b<len(ribs)-1):
                                fp.write("\n")
                            jatka = False
                        
                        
                d.get("https://vw4.viope.com/student/6314/#/content")
                fp.write(";")
                
                d.implicitly_wait(10)

def getAnswers():
    with open("answers.txt","r") as fp:
        return fp.read().split(";")
           
def doExercises(username,password,valinta):
    ribs = getAnswers()


    #Ribs on [title, koodi]

    
    for a in range(len(ribs)-1):
        vips = ribs[a].split("\n")
        kips = vips[0]
        vips.pop(0)
        vips='\n'.join(vips)
        ribs[a]=[kips,vips]
        
    d = SanomaProLogin(username,password)
    d.get("https://vw4.viope.com/student/6314/#/content")

    time.sleep(1)
    bs = BeautifulSoup(d.page_source,"html.parser")

    
    divit = []
    for x in bs.find_all("div",{"class":"course_expanded"}):
        for y in x.find_all("div",{"ng-repeat":"type in ex_types","class":"ng-scope"}):
            divit.append(y)
    
            
    for y in range(1,len(divit),4):
        for x in divit[y].find_all("span",{"class":"completion-not-started"}):
            
            if("Random" in x["title"].split(".")[0]):
                hips = 4
            else:
                hips = x["title"].split(".")[0]
            kakat = d.find_elements_by_class_name("btn-course")
            kakat[int(hips)-1].click()

            try:
                exa = '//span[@title="'+x["title"]+'"]'
                element = WebDriverWait(d, 10).until(
                EC.element_to_be_clickable((By.XPATH, exa))
                )
                element.click()
            except:
                pass
                
            for a in range(0,len(ribs)-1):
                if (x["title"] in ribs[a]):
                    action_chains = ActionChains(d)
                    codeMirror = WebDriverWait(d, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'CodeMirror'))
                    )
                    action_chains.click(codeMirror).perform()

                    print(ribs[a])
                    action_chains.send_keys(ribs[a][1].replace("\xa0","").replace("    ","")).perform()

                    if(valinta == "r"):
                        exa = '//button[contains(text(), "Run")]'
                        d.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    
                        element = WebDriverWait(d, 10).until(
                        EC.element_to_be_clickable((By.XPATH, exa))
                        )
                        element.click()
                    
                        exa = '//button[contains(text(), "Submit")]'
                        d.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    
                        element = WebDriverWait(d, 10).until(
                        EC.element_to_be_clickable((By.XPATH, exa))
                        )
                        element.click()
                    else:
                        exa = '//button[contains(text(), "Save")]'
                        d.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    
                        element = WebDriverWait(d, 10).until(
                        EC.element_to_be_clickable((By.XPATH, exa))
                        )
                        element.click()

                    d.get("https://vw4.viope.com/student/6314/#/content")
            
                    
                
            

            


    

def Main():
    #doExercises("","","r")
    #saveAnswers("","")
        

Main()

