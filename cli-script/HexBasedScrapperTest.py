import asyncio
import random
import json
import time
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import pytz
from datetime import datetime
import math
import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import datetime

# --------------------------------------------
# Twilio API Credentials for VoIP Call Alerts
# --------------------------------------------

# Description:
# The Twilio API credentials power the VoIP call alert functionality within your flight tracker system, ensuring critical updates 
# reach users promptly. These credentials enable integration with Twilio's robust communication platform, allowing for seamless
#  real-time voice notifications.

account_sid = ""
account_token = ""
alert_number = "+12184329666"

alert_radius = 150 # (In Miles)





# --------------------------------------------
# Bot Evading Tactics
# --------------------------------------------

# Description:
# Anti Bot evading tactics are implemented to prevent anti bot mechanisms from detecting  
# our web scrapping so that we can know the aircraft movements every 15 minutes without 
# raising flags

# --------------------------------------------
# User Agents Randomisation Data
# --------------------------------------------

# Description:
# User Agent randomisation is used to mask and vary the identity of requests made 
# to a server by simulating requests from different browsers or devices. This tactic 
# helps in preventing detection and blocking by server-side filters or security systems. 
# It ensures anonymity, evasion of detection mechanisms, and circumvents restrictions 
# based on known patterns of user agents.


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Android 10; SM-A505G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.110 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/92.0.902.73",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 12_5_1 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 11; SM-A526B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A716B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/86.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
    "Mozilla/5.0 (Android 10; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.0; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36"
]

# --------------------------------------------
# Fetching Current Month and Year
# --------------------------------------------

# Description:
# Fetching the current month and year for time modifier keyword for HTTP Header Referer
# which will create an impression of more 'natural' browsing keywords pattern in the HTTP Header's referer
# and Origin

today = datetime.datetime.now()
current_month_number = today.month
current_month_name = today.strftime("%B")  # Full month name
current_year = today.year

# --------------------------------------------
# Aircraft Registrations 
# --------------------------------------------

C17Registrations = ['VUAUA','VUAUB','VUAUC','VUAUD','VUAUE','VUAUF','VUAUG','VUAUH','VUAUI','VUAUJ','VUAUK']

# MixHexs = [{"CA-7106": "8016e5"},{"K5012":"8002f6"},{'VUAIL':"800e23"}]
MixHexs = [{"CA-7106": "8016e5"}, {"K5012": "8002f6"}, {'VUAIL':"800e23"}]


C295Hex = [{"CA-7106": "8016e5"}]
C130Hexs = [{'VUAIL':"800e23"}]
P8IHexs = [{'IN329':"800E8A"},{"IN328":"800E89"},{"IN327":"800313"},{"IN326":"800312"},{"IN325":"800311"},
{"IN324":"800310"},{"IN323":"80030F"},{"IN322":"80030E"},{"IN321":"80030D"},{"IN320":"80030C"}]
B737IndiaHexs = [{"K5012":"8002f6"}]

IAFPrivateJetsHexs = [{"VUAVV":"385b0ec1"}]
C17Hexs = [{"VUAUA":"80078E"},{"VUAUB":"80078F"},{"VUAUC":"800790"},{"VUAUD":"800791"},{"VUAUE":"800792"},{"VUAUF":"800793"},
{"VUAUG":"800794"},{"VUAUH":"800795"},{"VUAUI":"800796"},{"VUAUJ":"800797"},{"VUAUK":"800E63"},{"VUAUL":"8003C1"}]
An32Hexs = [{"VUMPG":"385aaf10"},{"VUDXD":"385b3e9e"}]
IL76Hexs = [{"K-2663":"8002D7"},{"K-2661":"8002D5"},{"K-2665":"8002D9"},{"KI2664":"8002D8"},
{"KI2666":"8002DA"},{"KI2878":"8002DB"},{"K-2879":"8002DC"}]
JaguarsHex = [{"JM255":"83F255"}]
AwacsHex = [{"VUAUM":"8003C1"},{"VTSCO":"8004FD"}]

testHexC295ADSB = "https://globe.adsbexchange.com/?icao=8016e5"

# --------------------------------------------
# Keyword Configuration Data
# --------------------------------------------

# Description:
# This section contains arrays of core keywords, intent modifiers, time modifiers, 
# and location-based keywords. These keywords are randomly combined to dynamically 
# generate search strings. This randomisation technique prevents predictable patterns, 
# making bot detection harder and improving query versatility by simulating varied 
# search behaviors and contexts.

core_keywords = ["C-17", "military aircraft", "Indian military aircrafts", "Navy","aircraft", "Globemaster", "C17 Globemaster", "Jet", "Indian Air Force", "Flight", "IAF", "C17", "Transport Plane"]
intent_modifiers = ["registration", "tracking", "monitoring", "flightpath", "movements", "air traffic", "track", "airspace", "update"]
time_modifiers = ["this week", "today", "history", "last 24 hours", "recent", "yesterday", datetime.datetime.now().strftime("%B"), str(datetime.datetime.now().year), "24 hours"]
location_keywords = ["Near Me", "India", "Bharat", "Gujarat", "Asia", "Tamil Nadu", "Jammu", "Kashmir", "Ladakh", "Rajasthan", "Kerala", "United States", "US"]


# --------------------------------------------
# Referer URL Configuration Data
# --------------------------------------------

# Description:
# This section defines a list of referer objects containing search engine URLs and their respective domains. 
# These URLs are dynamically used to randomize search patterns and simulate searches from different 
# sources. This randomization enhances variability in query requests and helps evade detection by 
# mimicking legitimate user traffic originating from various popular search engines.

REFERER_OBJECTS = [
    {"url": "https://www.bing.com/search?q={query}", "domain": "https://www.bing.com"},
    {"url": "https://www.google.com/search?q={query}", "domain": "https://www.google.com"},
    {"url": "https://search.yahoo.com/search?p={query}", "domain": "https://search.yahoo.com"},
    {"url": "https://duckduckgo.com/?q={query}", "domain": "https://duckduckgo.com"},
    {"url": "https://www.ecosia.org/search?q={query}", "domain": "https://www.ecosia.org"},
]

def weighted_random_choice(array):
    """Helper for selecting random elements."""
    return random.choice(array)

# --------------------------------------------
# Generate Search Query for Http Header Referer
# --------------------------------------------

def generate_search_query():
    """
    Generates a dynamic search query based on random combinations of keywords.
    """
    core = weighted_random_choice(core_keywords)
    intent = weighted_random_choice(intent_modifiers)
    time = weighted_random_choice(time_modifiers)
    location = weighted_random_choice(location_keywords)

    # Create contextually valid combinations
    if random.random() > 0.5:
        # Case 1: Core + Intent + Time
        search_term = f"{core} {intent} {time}"
    else:
        # Case 2: Core + Intent + Location + Time
        search_term = f"{core} {intent} {location} {time}"

    # Sanitize/URL-encode query (basic encoding)
    search_term = search_term.replace(" ", "+")
    print(f"Generated Search Query: {search_term}")
    return search_term


# --------------------------------------------
# ASCII Header when the script starts up
# -------------------------------------------- 

def print_stylized_header():
    # Green border escape code
    GREEN = "\033[32m"
    RESET = "\033[0m"
    
    border = GREEN + "+" + "=" * 70 + "+" + RESET
    title = "🚀 FlyWatch Aircraft Movement Detection System 🚀"
    author = "Code by Roshan Bhatia"
    ig_handle = "IG: @2kwattz"
    
    # Print the header with green border only
    print("\n")
    print(border)
    print(f"| {title.center(70)} |")
    print("|" + " " * 72 + "|")
    print(f"| {author.center(70)} |")
    print(f"| {ig_handle.center(70)} |")
    print(border)
    print("\n")
    time.sleep(3)


print_stylized_header()

def get_random_referer_and_origin():
    selected = random.choice(REFERER_OBJECTS)
    referer_url = selected["url"]  # URL for Referer
    origin_domain = selected["domain"]  # Domain for Origin
    print(f"Random HTTPS Header Referer & Origin Generated\n")
    print("Random User Agent String Generated\n")
    return referer_url, origin_domain

# HTTPS Headers for Scrapping request

def generateHeaders():       
       referer, origin = get_random_referer_and_origin()
       query = generate_search_query()
       
       selected_referer_template = random.choice(REFERER_OBJECTS)
       referer_url = selected_referer_template["url"].replace("{query}", query)

       print("referer_url", referer_url)
       HEADERS = {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": referer_url,  # Randomize the Referer
        "Accept-Language": random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.8", "en-AU,en;q=0.7"]),
        "DNT": str(random.choice([0,1])), # DNT Really Doesnt matter
        "Upgrade-Insecure-Requests": str(random.choice([0,1])),
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "no-cache",
        "Origin": origin,
    }
       
       print("Dynamic Headers", HEADERS,"\n")
       return HEADERS



def dataScrapper():
    httpHeader = generateHeaders()
    with sync_playwright() as p:
        # Launch a headless browser
        browser = p.chromium.launch(headless=False,
         args=['--use-gl=egl'])  # Set headless=False for visible scraping
        page = browser.new_page()

        # Apply stealth settings to the page
        # stealth_sync(page)

        page.set_extra_http_headers(httpHeader)
 
        # Navigate to the target website
        # page.goto('https://www.airnavradar.com/data/flights/VUAUA',wait_until='load',timeout=120000)
        page.goto(testHexC295ADSB, wait_until="load",timeout=120000)
        # page.wait_for_load_state('networkidle', timeout=60000)

        page.wait_for_selector("#selected_position")

        selected_position_text = page.locator("#selected_position").inner_text()
        time.sleep(800)
        # Print the extracted text
        print(f"C295 CA-710 Position IN LAT LONG: {selected_position_text}")

    

        # Close the browser
        browser.close()

dataScrapper()



