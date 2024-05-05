from browsermobproxy import Server
from selenium import webdriver
from seleniumwire import webdriver

# Chrome webdriver with Selinium Wire capabilities 
driver = webdriver.Chrome(options=webdriver.ChromeOptions())
driver.get('https://www.flightaware.com/live/flight/VUAUB')
