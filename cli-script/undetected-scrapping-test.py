import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import random
from bs4 import BeautifulSoup

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://www.radarbox.com/data/flights/VUAUB")

# Find an element on the page to move the mouse to
response = driver.page_source
time.sleep(2)
soup = BeautifulSoup(response, 'html.parser')
print(soup)

actions = ActionChains(driver)

# Randomize mouse movements and clicks
for _ in range(5):
    # Move mouse to a random position relative to the element
    x_offset = random.randint(100, 500)
    y_offset = random.randint(100, 500)
    actions.move_to_element_with_offset(element, x_offset, y_offset)
    
    # Perform a click at the current mouse position
    actions.click()
    
    # Perform the actions
    actions.perform()
    
    # Pause execution for a random duration (0.5 to 2 seconds)
    time.sleep(random.uniform(0.5, 2))
    
driver.quit()
