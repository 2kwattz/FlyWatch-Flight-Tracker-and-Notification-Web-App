import asyncio
import random
import json
import time
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_async
import pytz
from datetime import datetime
import math
import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse




# User Agents

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

# Referer List to fool the Bot Detection Mechanism 

# REFERER_LIST = [
#     "https://www.bing.com/search?q=airnav+radar",
#     "https://www.airlinegeeks.com/",
#     "https://www.bing.com/search?q=C-17+tracking+registrations",
#     "https://www.google.com/search?q=C-17+registration+tracking",
#     "https://twitter.com/FlightGlobal",
#     "https://www.google.com/search?q=C-17+aircraft+tracking",
#     "https://search.yahoo.com/search?p=C-17+aircraft+tracking",
#     "https://www.google.com/search?q=C-17+airbase+movements",
#     "https://www.lockheedmartin.com/en/capabilities/c-17-globemaster-iii.html",
#     "https://www.google.com/search?q=C-17+registration+lookup",
#     "https://twitter.com/search?q=C-17+registration+tracking",
#     "https://twitter.com/search?q=military+aircraft+C-17",
#     "https://www.qwant.com/?q=C-17+tracking",
#     "https://startpage.com/sp/search?q=C-17+aircraft+tracking",
#     "https://www.ecosia.org/search?q=C-17+movements",
#     "https://www.search.com/search?q=C-17+airbase+movements",
#     "https://twitter.com/aviationdaily",
#     "https://twitter.com/DefenseNews",
#     "https://duckduckgo.com/?q=C-17+registration+tracking",
#     "https://www.aviationweek.com/",
#     "https://duckduckgo.com/?q=C-17+aircraft+tracking",
#     "https://twitter.com/search?q=C-17+aircraft+tracking",
#     "https://duckduckgo.com/?q=track+C-17+registration",
#     "https://search.yahoo.com/search?p=C-17+registration+tracking+Indian+Air+Force",
#     "https://duckduckgo.com/",
#     "https://www.facebook.com/",
# ]

REFERER_OBJECTS = [
    {"url": "https://www.bing.com/search?q=airnav+radar", "domain": "https://www.bing.com"},
    {"url": "https://www.airlinegeeks.com/", "domain": "https://www.airlinegeeks.com"},
    {"url": "https://www.bing.com/search?q=C-17+tracking+registrations", "domain": "https://www.bing.com"},
    {"url": "https://www.google.com/search?q=C-17+registration+tracking", "domain": "https://www.google.com"},
    {"url": "https://twitter.com/FlightGlobal", "domain": "https://twitter.com"},
    {"url": "https://www.google.com/search?q=C-17+aircraft+tracking", "domain": "https://www.google.com"},
    {"url": "https://search.yahoo.com/search?p=C-17+aircraft+tracking", "domain": "https://search.yahoo.com"},
    {"url": "https://www.google.com/search?q=C-17+airbase+movements", "domain": "https://www.google.com"},
    {"url": "https://www.lockheedmartin.com/en/capabilities/c-17-globemaster-iii.html", "domain": "https://www.lockheedmartin.com"},
    {"url": "https://www.google.com/search?q=C-17+registration+lookup", "domain": "https://www.google.com"},
    {"url": "https://twitter.com/search?q=C-17+registration+tracking", "domain": "https://twitter.com"},
    {"url": "https://twitter.com/search?q=military+aircraft+C-17", "domain": "https://twitter.com"},
    {"url": "https://www.qwant.com/?q=C-17+tracking", "domain": "https://www.qwant.com"},
    {"url": "https://startpage.com/sp/search?q=C-17+aircraft+tracking", "domain": "https://startpage.com"},
    {"url": "https://www.ecosia.org/search?q=C-17+movements", "domain": "https://www.ecosia.org"},
    {"url": "https://www.search.com/search?q=C-17+airbase+movements", "domain": "https://www.search.com"},
    {"url": "https://twitter.com/aviationdaily", "domain": "https://twitter.com"},
    {"url": "https://twitter.com/DefenseNews", "domain": "https://twitter.com"},
    {"url": "https://duckduckgo.com/?q=C-17+registration+tracking", "domain": "https://duckduckgo.com"},
    {"url": "https://www.aviationweek.com/", "domain": "https://www.aviationweek.com"},
    {"url": "https://duckduckgo.com/?q=C-17+aircraft+tracking", "domain": "https://duckduckgo.com"},
    {"url": "https://twitter.com/search?q=C-17+aircraft+tracking", "domain": "https://twitter.com"},
    {"url": "https://duckduckgo.com/?q=track+C-17+registration", "domain": "https://duckduckgo.com"},
    {"url": "https://search.yahoo.com/search?p=C-17+registration+tracking+Indian+Air+Force", "domain": "https://search.yahoo.com"},
    {"url": "https://duckduckgo.com/", "domain": "https://duckduckgo.com"},
    {"url": "https://www.facebook.com/", "domain": "https://www.facebook.com"},
]


def get_random_referer_and_origin():
    selected = random.choice(REFERER_OBJECTS)
    referer_url = selected["url"]  # URL for Referer
    origin_domain = selected["domain"]  # Domain for Origin

    print(f"Random Referer Generated {referer_url} \n Coressponding Domain {origin_domain}")
    return referer_url, origin_domain



# HTTPS Headers for Scrapping request

def generateHeaders():
       
       referer, origin = get_random_referer_and_origin()
       HEADERS = {
        "User-Agent": random.choice(USER_AGENTS), # Randomize User-Agent
        "Referer": referer,  # Randomize the Referer
        # "Accept-Language":  # Coz I need english
        "Accept-Language": random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.8", "en-AU,en;q=0.7"]),
        "DNT": str(random.choice([0,1])), # DNT Really Doesnt matter
        "Upgrade-Insecure-Requests": str(random.choice([0,1])),
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "no-cache",
        "Origin": origin,
    }
       return HEADERS
