import undetected_chromedriver as uc
uc.install()
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import random
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from multiprocessing import Pool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
 
cwd = os.getcwd()

opts = webdriver.ChromeOptions()
opts.headless = True
opts.add_argument('log-level=3') 
dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
opts.add_argument('--ignore-ssl-errors=yes')
#opts.add_argument("--start-maximized")
opts.add_argument("window-size=200,100")
opts.add_argument('--ignore-certificate-errors')
opts.add_argument('--disable-blink-features=AutomationControlled')
opts.add_experimental_option('excludeSwitches', ['enable-logging'])

def xpath_type(el,mount):
    return wait(browser,10).until(EC.presence_of_element_located((By.XPATH, el))).send_keys(mount)

def xpath_el(el):
    element_all = wait(browser,30).until(EC.presence_of_element_located((By.XPATH, el)))
    
    return browser.execute_script("arguments[0].click();", element_all)

def view_channel():
    file_list = "channel.txt"
    myfile = open(f"{cwd}/{file_list}","r")
    shop = myfile.read()
    list_url = shop.split("\n")
    browser.get(list_url[0])
    like_vid = wait(browser,10).until(EC.presence_of_element_located((By.XPATH,'((//button[@aria-pressed]))[6]')))
    check_like = like_vid.get_attribute('aria-pressed')
    #print(check_like)
    if "true" in str(check_like):
        print(f"[{time.strftime('%d-%m-%y %X')}] Already Like Video Success")
    elif "false" in str(check_like):
        xpath_el('(//yt-icon-button[@class="style-scope ytd-toggle-button-renderer style-text"])[1]')
        print(f"[{time.strftime('%d-%m-%y %X')}] Like Video Success")
    
    sub_vid = wait(browser,10).until(EC.presence_of_element_located((By.XPATH,'//tp-yt-paper-button[@class="style-scope ytd-subscribe-button-renderer"]')))
    check_sub = sub_vid.get_attribute('aria-label')
    #print(check_sub)
    if "Unsubscribe" in str(check_sub):
        print(f"[{time.strftime('%d-%m-%y %X')}] Already Subscribe Channel")
        pass
    else:
        xpath_el('//tp-yt-paper-button[@class="style-scope ytd-subscribe-button-renderer"]')
        print(f"[{time.strftime('%d-%m-%y %X')}] Subscribe Channel Success")
    browser.quit()
    sleep(5)
     

def login():
    global element
    global browser
          
    sleep(5)

    element = wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#identifierId")))
    element.send_keys(email)
        
    sleep(0.5)
    element.send_keys(Keys.ENTER) 
    sleep(3)  
    try:
        element = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
        
        element.send_keys(password)
        sleep(0.5)
        element.send_keys(Keys.ENTER) 
    except:
        sleep(3)
        element = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
        
        element.send_keys(password)
        sleep(0.5)
        element.send_keys(Keys.ENTER) 
    try: 
        wait(browser,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#accept"))).click()
    except:
        pass
    try:
        sleep(10)
        view_channel()
    except Exception as e:
        sleep(2)
        


def open_browser(k):
    
    global browser
    global element
    global email
    global password
    k = k.split(",")
    email = k[0]
    password = k[1]
    random_angka = random.randint(100,999)
    random_angka_dua = random.randint(10,99)
    opts.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.{random_angka}.{random_angka_dua} Safari/537.36")
    browser = webdriver.Chrome(options=opts, desired_capabilities=dc)
    browser.get("https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=en&ec=65620&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
    try:
        login()
    except Exception as e:
        print(f"[{time.strftime('%d-%m-%y %X')}] [ {email} ] Failed Login, Error: {e}")
        with open('failed.txt','a') as f:
            f.write('{0}|{1}\n'.format(email,password))
        browser.quit()
if __name__ == '__main__':
    global list_accountsplit
    print(f"[{time.strftime('%d-%m-%y %X')}] Automation Like and Subs Streaming YT")
    url_input = input(f"[{time.strftime('%d-%m-%y %X')}] Input 1 URL: ")
    
    with open('channel.txt','w') as f:
        f.write('{0}\n'.format(url_input))
    jumlah = int(input(f"[{time.strftime('%d-%m-%y %X')}] Multi Processing: "))
    file_list_akun = "email_acc.txt"
    myfile_akun = open(f"{cwd}/{file_list_akun}","r")
    akun = myfile_akun.read()
    list_accountsplit = akun.split("\n")
    k = list_accountsplit

    with Pool(jumlah) as p:  
        p.map(open_browser, k)
   
