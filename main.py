from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pyperclip

def waitElemc(d, exa):

    #Wait for element to be clickable
    element = WebDriverWait(d, 10).until(
    EC.element_to_be_clickable((By.XPATH, exa))
    )
    return element
def waitElem(d, exa):
    
    #Waits for element to be found
    element = WebDriverWait(d, 10).until(
    EC.presence_of_element_located((By.XPATH, exa))
    )
    return element

def SanomaProLogin(username, password):
    
    url = "https://kirjautuminen.sanomapro.fi/sso/XUI/#login/&realm=%2Fratkoo"

    d = webdriver.Chrome("chromedriver.exe")

    d.get(url)
    d.implicitly_wait(10)


    # Saatat kysyä MIKÄ IHMEEN EXA ? No pakko venaa elementti ennenkun sen kaa voi leikkii!
    
    waitElem(d,'//input[@id="username"]').send_keys(username)            
    waitElem(d,'//input[@id="password"]').send_keys(password)               
    waitElem(d,'//input[@id="loginButton_0"]').click()

    time.sleep(3)        
    
    d.get("https://oppimisymparisto.sanomapro.fi/d2l/le/content/custom/1545693/57176258/Viewer")
    
    time.sleep(3)

    return d

def saveAnswers(username, password):
    
    d = SanomaProLogin(username,password)
    d.get("https://vw4.viope.com/student/6314/#/content")

    time.sleep(1)
    bs = BeautifulSoup(d.page_source,"html.parser")



    #Löydetään oikea div alue neljstä ->
    
    divit = []
    for x in bs.find_all("div",{"class":"course_expanded"}):
        for y in x.find_all("div",{"ng-repeat":"type in ex_types","class":"ng-scope"}):
            divit.append(y)
    #<--
            
            
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
                
                waitElem(d,'//span[@title="'+x["title"]+'"]').click()
                
                waitElem(d,'//button[@ng-click="showExampleAnswer()"]').click()

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


    #Ribs on [title, koodi, title,...]

    
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
    
            waitElemc(d,'//span[@title="'+x["title"]+'"]').click()
                
            for a in range(0,len(ribs)-1):
                if (x["title"] in ribs[a]):

                    
                    action_chains = ActionChains(d)
                    
                    codeMirror = WebDriverWait(d, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'CodeMirror'))
                    )
                    action_chains.click(codeMirror).perform()

                    koodi = ribs[a][1]
                    print(ribs[a])
                    pyperclip.copy(koodi)
        
                    action_chains.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()

                    
                    

                    if(valinta == "r"):

                        
                        d.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    
                        waitElem(d,'//button[contains(text(), "Run")]').click()

                        d.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    
                        waitElem(d,'//button[contains(text(), "Submit")]').click()

                        
                    else:
                        
                        d.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        
                        waitElem(d,'//button[contains(text(), "Save")]').click()

                    d.get("https://vw4.viope.com/student/6314/#/content")
            
                    
                
            

            


    

def Main():
    #doExercises("usr","pass","r")
    #saveAnswers("usr","pass")
        

Main()

