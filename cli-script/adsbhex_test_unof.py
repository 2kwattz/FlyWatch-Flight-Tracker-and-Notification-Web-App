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
import math
import json

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

alert_radius = 150 # Defalut radius (In Miles)


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
#  Calculate Distance Between Two Geographical
#  Points and Check if Within Radius
# --------------------------------------------

# Description:
#This function calculates the distance between two geographical coordinates (latitude and longitude)
#using the Haversine formula and checks if the distance is within a given radius (in miles).
#The function returns True if the distance is within the specified radius, otherwise False.

def is_within_radius(lat1, lon1, lat2, lon2, radius):
    # Haversine formula to calculate the distance between two points
    def to_radians(degree):
        return degree * (math.pi / 180)

    R = 3958.8  # Radius of Earth in miles (mean radius)
    lat1_rad = to_radians(lat1)
    lon1_rad = to_radians(lon1)
    lat2_rad = to_radians(lat2)
    lon2_rad = to_radians(lon2)

    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = (math.sin(delta_lat / 2) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) *
         math.sin(delta_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c  # Distance in miles

    # Check if the distance is within the radius
    return distance <= radius

# Example usage
lat1 = 28.7041  # Latitude of point 1 (e.g., New Delhi)
lon1 = 77.1025  # Longitude of point 1
lat2 = 19.0760  # Latitude of point 2 (e.g., Mumbai)
lon2 = 72.8777  # Longitude of point 2
radius = 500    # Radius in miles

result = is_within_radius(lat1, lon1, lat2, lon2, radius)

# --------------------------------------------
# Aircraft Registrations 
# --------------------------------------------

C17Registrations = ['VUAUA','VUAUB','VUAUC','VUAUD','VUAUE','VUAUF','VUAUG','VUAUH','VUAUI','VUAUJ','VUAUK']

# MixHexs = [{"CA-7106": "8016e5"},{"K5012":"8002f6"},{'VUAIL':"800e23"}]
MixHexs = [{"CA-7106": "8016e5"}, {"K5012": "8002f6"}, {'VUAIL':"800e23"}]


C295Hex = [{"CA-7106": "8016e5"}]
C130Hexs = [{'VUAIL':"800e23"}]
P8IHexs = [
  {"Callsign": "IN329", "AircraftName": "P8i", "AircraftOperator": "IndianNavy", "HexCode": "800E8A", "isNearUserSpecifiedCity": False},
  {"Callsign": "IN328", "AircraftName": "P8i", "AircraftOperator": "IndianNavy", "HexCode": "800E89", "isNearUserSpecifiedCity": False},
  {"Callsign": "IN327", "AircraftName": "P8i", "AircraftOperator": "IndianNavy", "HexCode": "800313", "isNearUserSpecifiedCity": False},
  {"Callsign": "IN326", "AircraftName": "P8i", "AircraftOperator": "IndianNavy", "HexCode": "800312", "isNearUserSpecifiedCity": False},
  {"Callsign": "IN325", "AircraftName": "P8i", "AircraftOperator": "IndianNavy", "HexCode": "800311", "isNearUserSpecifiedCity": False},
  {"Callsign": "IN324", "AircraftName": "P8i", "AircraftOperator": "IndianNavy", "HexCode": "800310", "isNearUserSpecifiedCity": False},
  {"Callsign": "IN323", "AircraftName": "P8i", "AircraftOperator": "IndianNavy", "HexCode": "80030F", "isNearUserSpecifiedCity": False},
  {"Callsign": "IN322", "AircraftName": "P8i", "AircraftOperator": "IndianNavy", "HexCode": "80030E", "isNearUserSpecifiedCity": False},
  {"Callsign": "IN321", "AircraftName": "P8i", "AircraftOperator": "IndianNavy", "HexCode": "80030D", "isNearUserSpecifiedCity": False},
  {"Callsign": "IN320", "AircraftName": "P8i", "AircraftOperator": "IndianNavy", "HexCode": "80030C", "isNearUserSpecifiedCity": False},
  {"Callsign": "IN330", "AircraftName": "P8i", "AircraftOperator": "IndianNavy", "HexCode": "800E8B", "isNearUserSpecifiedCity": False},
  {"Callsign": "IN331", "AircraftName": "P8i", "AircraftOperator": "IndianNavy", "HexCode": "800E8C", "isNearUserSpecifiedCity": False}
]

# B737IndiaHexs = [{"K5012":"8002f6"}]

IAFPrivateJetsHexs = [{"VUAVV":"385b0ec1"}]
C17Hexs = [
  {"Callsign": "VUAUA", "AircraftName": "C17", "AircraftOperator": "IndianAirForce", "HexCode": "80078E", "isNearUserSpecifiedCity": False},
  {"Callsign": "VUAUB", "AircraftName": "C17", "AircraftOperator": "IndianAirForce", "HexCode": "80078F", "isNearUserSpecifiedCity": False},
  {"Callsign": "VUAUC", "AircraftName": "C17", "AircraftOperator": "IndianAirForce", "HexCode": "800790", "isNearUserSpecifiedCity": False},
  {"Callsign": "VUAUD", "AircraftName": "C17", "AircraftOperator": "IndianAirForce", "HexCode": "800791", "isNearUserSpecifiedCity": False},
  {"Callsign": "VUAUE", "AircraftName": "C17", "AircraftOperator": "IndianAirForce", "HexCode": "800792", "isNearUserSpecifiedCity": False},
  {"Callsign": "VUAUF", "AircraftName": "C17", "AircraftOperator": "IndianAirForce", "HexCode": "800793", "isNearUserSpecifiedCity": False},
  {"Callsign": "VUAUG", "AircraftName": "C17", "AircraftOperator": "IndianAirForce", "HexCode": "800794", "isNearUserSpecifiedCity": False},
  {"Callsign": "VUAUH", "AircraftName": "C17", "AircraftOperator": "IndianAirForce", "HexCode": "800795", "isNearUserSpecifiedCity": False},
  {"Callsign": "VUAUI", "AircraftName": "C17", "AircraftOperator": "IndianAirForce", "HexCode": "800796", "isNearUserSpecifiedCity": False},
  {"Callsign": "VUAUJ", "AircraftName": "C17", "AircraftOperator": "IndianAirForce", "HexCode": "800797", "isNearUserSpecifiedCity": False},
  {"Callsign": "VUAUK", "AircraftName": "C17", "AircraftOperator": "IndianAirForce", "HexCode": "800E63", "isNearUserSpecifiedCity": False},
  {"Callsign": "VUAUL", "AircraftName": "C17", "AircraftOperator": "IndianAirForce", "HexCode": "8003C1", "isNearUserSpecifiedCity": False}
]



IL76Hexs = [
  {"Callsign": "K-2663", "AircraftName": "IL76", "AircraftOperator": "IndianAirForce", "HexCode": "8002D7", "isNearUserSpecifiedCity": False},
  {"Callsign": "K-2661", "AircraftName": "IL76", "AircraftOperator": "IndianAirForce", "HexCode": "8002D5", "isNearUserSpecifiedCity": False},
  {"Callsign": "K-2665", "AircraftName": "IL76", "AircraftOperator": "IndianAirForce", "HexCode": "8002D9", "isNearUserSpecifiedCity": False},
  {"Callsign": "KI2664", "AircraftName": "IL76", "AircraftOperator": "IndianAirForce", "HexCode": "8002D8", "isNearUserSpecifiedCity": False}
]


JaguarsHex = [
  {"Callsign": "JM255", "AircraftName": "Jaguar", "AircraftOperator": "IndianAirForce", "HexCode": "83F255", "isNearUserSpecifiedCity": False}
]

AwacsHex = [{"VUAUM":"8003C1"},{"VTSCO":"8004FD"}]

An32Hexs = [
  {"Callsign": "VUMPG", "AircraftName": "An32", "AircraftOperator": "IndianAirForce", "HexCode": "385aaf10", "isNearUserSpecifiedCity": False},
  {"Callsign": "VUDXD", "AircraftName": "An32", "AircraftOperator": "IndianAirForce", "HexCode": "385b3e9e", "isNearUserSpecifiedCity": False}
]
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
        # "Referer": referer_url,  # Randomize the Referer
        "Accept-Language": random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.8", "en-AU,en;q=0.7"]),
        "DNT": str(random.choice([0,1])), # DNT Really Doesnt matter
        "Upgrade-Insecure-Requests": str(random.choice([0,1])),
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "no-cache",
        "Origin": origin,
    }
       
       print("Dynamic Headers", HEADERS,"\n")
       return HEADERS

# def capture_response(response):
#     # Check if the response is from the API you're interested in
#     if "api.adsb.lol" in response.url:
#         # Print URL, status, and parse JSON body
#         print(f"Response URL: {response.url}")
#         print(f"Response Status: {response.status}")  # Ensure this is not overwritten by an int somewhere
#         try:
#             json_data = response.json()  # Get JSON content from the response
#             return json_data
            
#         except Exception as e:
#             print(f"Failed to parse JSON: {str(e)}")
#             return e

# def dataScrapper():
#     httpHeader = generateHeaders()
#     with sync_playwright() as p:
#         # Launch a headless browser
#         browser = p.chromium.launch(headless=False, args=['--use-gl=egl'])  # Set headless=False for visible scraping
#         page = browser.new_page()
#         page.on("response", capture_response)

#         # Apply stealth settings to the page
#         # stealth_sync(page)

#         page.set_extra_http_headers(httpHeader)

#         for hex in P8IHexs:
#             aircraftHex = hex['HexCode']
#             page.goto(f"https://api.adsb.lol/v2/icao/{aircraftHex}", wait_until="load", timeout=120000)
#             time.sleep(5)

#         # Close the browser
#         browser.close()

# dataScrapper()


# Shared list to hold the responses

def capture_response(response, P8IHexs):

    if "api.adsb.lol" in response.url:
        print(f"Response URL: {response.url}")
        print(f"Response Status: {response.status}") 
        try:
            
            json_data = response.json()  
           
            for hex in P8IHexs:
                if hex['HexCode'] in response.url:
                    print(f"Processing for HexCode: {hex['HexCode']}")
                    process_response_data(json_data, hex)
        except Exception as e:
            print(f"Failed to parse JSON: {str(e)}")

def process_response_data(json_data, hex_data):

    print(f"Processing response data for {hex_data['HexCode']}: {json.dumps(json_data, indent=2)}")

    print("JSON DATA.AC", json_data["ac"])
    if 'icao' in json_data:
        print(f"Aircraft ICAO: {json_data['icao']} for HexCode: {hex_data['HexCode']}")


def dataScrapper():
    httpHeader = generateHeaders()
    with sync_playwright() as p:
        # Launch a headless browser
        browser = p.chromium.launch(headless=False, args=['--use-gl=egl'])  # Set headless=False for visible scraping
        page = browser.new_page()
        page.on("response", lambda response: capture_response(response, P8IHexs))  # Pass P8IHexs with the response

        # Apply stealth settings to the page
        # stealth_sync(page)

        page.set_extra_http_headers(httpHeader)

        for hex in P8IHexs:
            aircraftHex = hex['HexCode']
            print(f"Navigating to: https://api.adsb.lol/v2/icao/{aircraftHex}")
            page.goto(f"https://api.adsb.lol/v2/icao/{aircraftHex}", wait_until="load", timeout=120000)
            time.sleep(5)  

        # Close the browser
        browser.close()

dataScrapper()
