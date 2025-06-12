#Ticket Scraper Final

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.proxy import *
from lxml import etree
from bs4 import BeautifulSoup
import json
import requests
import chromedriver_binary
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import time
import csv
from datetime import date
from datetime import datetime
from datetime import timedelta
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from pathlib import Path
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
print('Current directory:' + current_dir)
sys.path.append(current_dir)

import importlib.util

# Get the absolute path to the module
module_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "utils.py")

# Create a module spec from the path
spec = importlib.util.spec_from_file_location("utils", module_path)

# Create a module from the spec
module = importlib.util.module_from_spec(spec)

# Execute the module in the module namespace
spec.loader.exec_module(module)




#STEP 1 (enter the date for the game you want to record)

hs = pd.read_csv(current_dir +'/GameTicketPromotionPrice.csv')
hs['BOTH'] = hs['START DATE'] + ',' + hs['START TIME']

hs['BOTH'] = pd.to_datetime(hs['BOTH'], format='%m/%d/%y,%I:%M %p')
hs['START DATE'] = pd.to_datetime(hs['START DATE'], format='%m/%d/%y')
hs = hs[hs['BOTH'] >= datetime.today()]

date_str = input('Desired Ticket Day (Format MM-DD-YYYY)\n')
date_ob = datetime.strptime(date_str, '%m-%d-%Y')

file_str = input('Filepath for output, ending with \'yourgame.csv\'\n')



#The website only lists future games, so have to get the index dynamically using a schedule of games (/GameTicketPromotionPricetytyt)
i_list = hs.index[hs['START DATE'] == date_ob].to_list()
today_i = hs.index[0]
master_i = i_list[0] - today_i + 1
print(master_i)
filename = file_str
    






# Step 2.1 Navigate to braves ticket url for input date
#Will timeout after a 3 or so attempts, or too many automated actions
url = 'https://www.mlb.com/braves/tickets/single-game-tickets'

#Accept cookies then click button for desired date
def start_driver(url) :


    chrome_options = webdriver.ChromeOptions()
    

    #Remove Automation Flags
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    

    #Begin webdrive Instance
    d = webdriver.Chrome(options=chrome_options)
    #Change propert of navigator for webdriver to undefined
    d.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")



    d.get(url)
    return d
    
d = start_driver(url) 
cookies = '//*[@id="onetrust-accept-btn-handler"]'


#master_i corresponds to button on webpage, derived from game date
#ticketX = '//*[@id="__next"]/main/div[2]/div/div/div[2]/div/div/div/div/div[2]/div[' + str(master_i) + ']/div[1]/div[3]/div[3]/a'
ticketX = '//*[@id="__next"]/div/main/div[2]/div/div/div[2]/div/div/div/div[3]/div[2]/div[' + str(master_i) + ']/div/div[3]/div[3]/a'

print(ticketX)
time.sleep(5)
d.find_element(By.XPATH, cookies).click()
time.sleep(7)
d.find_element(By.XPATH, ticketX).click()
time.sleep(7)





#Step 2.2 Toggle Tabs
p = d.current_window_handle

#get first child window
chwd = d.window_handles

for w in chwd:
#switch focus to child window
    if(w!=p):
        d.switch_to.window(w)
        break
        
time.sleep(3)
print("Child window title: " + d
      .title)

#When tickets are scarce, there is an intermediate webpage that needs to be addressed, put this is try block
try:
    mid_button = d.find_element(By.XPATH, '//*[@id="gm778464"]/div[2]/div/div/a/button/span')
    mid_button.click()

except (NoSuchElementException, ElementNotInteractableException  ) as e :
    print('No button')




time.sleep(3)


p2 = d.current_window_handle

#get first child window
chwd = d.window_handles

for w in chwd:
#switch focus to child window
    
    if(w!=p and w!=p2):
        d.switch_to.window(w)
        break
        
time.sleep(7)
print("Child window title: " + d
      .title)


# #Click agree button
agree_button = d.find_element(By.XPATH, '//*[@id=":r1:"]/div[2]/button')


agree_button.click()









#Step 2.3 Open Second webpage to get price data for all sections 
d2= webdriver.Chrome()
d2.get('https://www.mlb.com/braves/tickets/pricing')
time.sleep(3)
cookies = '//*[@id="onetrust-accept-btn-handler"]'
d2.find_element(By.XPATH, cookies).click()
soup = BeautifulSoup(d2.page_source, 'html.parser')
price_table = soup.find('table', class_='pricing__table prices')
d2.quit()

#Getting prices for the correct date and saving it in price_list
price_list = []

for row in price_table.tbody.find_all('tr'): 
        # Find all data for each column
    columns = row.find_all('td')
    if(columns != []):
        sec_price = columns[master_i -1]
        if (sec_price.text != '') :
            final = float(sec_price.text.strip('$'))
            price_list.append(final)





#Step 2.4 Hover over each section
#Loop to get ticket prices for every section
cat = ''
price_hist = ''
counter = 1
while (counter < 254) :
    
    sec_241 = '#map-container > div.zoomer > div.map__zoomer > svg > g.polygons > path:nth-child(' + str(counter) +')'
    action = ActionChains(d)
    polygon = d.find_element(By.CSS_SELECTOR, sec_241)
    action.move_to_element(polygon).perform()
    #print(polygon.get_attribute('data-section-name'))
    section = polygon.get_attribute('data-section-name')
    
    #Loop to get ticket prices for 3 sections
    #Get ticket price information

    #Something is wrong with my indexing, the position of seats available changes with each section
    #Get ticket price information and make sure sections without tickets don't register for numtix
    #still doesn't catch general admission sections where tickets arn't listed, i guess that's okay because those tickets arn't scarce
    soup1 = BeautifulSoup(d.page_source, 'html.parser')
    elements = soup1.find_all(id= 'map-container')
    children = elements[0].findChildren()
    kids = children[0].findChildren()
    
    if (len(kids) >0) :
        
        final = kids[-1].text
        if (len(final) > 0) :
            
            test = final.split()
        
            #Makes sure we only record numbers for an element describing number of tickets
            if (test[-1] == "Tickets"):
                numtix = final[0:2]
            else:
                numtix = None
        
        else:
            numtix = None
        
        #Step 2.5 Use historical data to assign comparison price, assign label to section, and assign actual current price
        pch = module.assign_price(section, price_list)
        
        section = section.split(',')[0]
        
        newline = str(section) + ',' + str(numtix) + ',' + pch + ',' + str(date.today())
        tix_file = open(filename, 'a')
        tix_file.write(newline)
        tix_file.write('\n')
        tix_file.close()
        


        time.sleep(7)
    counter += 1
d.quit()


