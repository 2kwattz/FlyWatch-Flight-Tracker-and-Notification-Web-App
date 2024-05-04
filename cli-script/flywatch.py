# Fly Watch Python CLI based script 
# Code Author : Roshan Bhatia. Instagram : @2kwattz . Github : 2kwattz

import pyfiglet
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


api_sources = {
    'ADBS_EXCHANGE' : '',
    'RADARBOX' : 'https://www.radarbox.com/',
    'FR24' : '',
    'AviationStack' : 'https://aviationstack.com/'
}

# Local Databases

class C17:
    def __init__(self,model,registration,country):
        self.model = model
        self.registration = registration
        self.country = country
        self.lastInitial = registration[-1]
    
# Initialize Models

VUAUA = C17("C17","VUAUA","India")
VUAUB = C17("C17","VUAUB","India")
VUAUD = C17("C17","VUAUD","India")
VUAUH = C17("C17","VUAUH","India")
VUAUJ = C17("C17","VUAUJ","India")
VUAUK = C17("C17","VUAUK","India")
VUAUL = C17("C17","VUAUL","India")

C17_instances = [VUAUA,VUAUB,VUAUD,VUAUH,VUAUJ,VUAUK,VUAUL]
# Location

# Keeping a static endpoint temporarily



chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
# Assuming you have Chrome WebDriver installed.
driver = webdriver.Chrome(options=chrome_options)

# Setting up user agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")

for instances in C17_instances:
    
    reg = instances.lastInitial
    flight_map = "https://www.radarbox.com/@21.73193,73.27099,z8"
    flight_history = f'https://www.radarbox.com/data/flights/VUAU{reg}'
    print(flight_history)
    driver.get(flight_history)

driver.get(flight_map)
page_source = driver.page_source
# print(page_source)
soup = BeautifulSoup(page_source, 'html.parser')
aircraft_of_interest = soup.find(id='#')

