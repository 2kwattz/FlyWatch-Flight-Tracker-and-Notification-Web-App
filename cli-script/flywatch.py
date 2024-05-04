# Fly Watch Python CLI based script 
# Code Author : Roshan Bhatia. Instagram : @2kwattz . Github : 2kwattz
import pyfiglet
import requests

api_sources = {
    'ADBS_EXCHANGE' : '',
    'RADARBOX' : 'https://www.radarbox.com/',
    'FR24' : '',
    'AviationStack' : 'https://aviationstack.com/'
}

# Local Databases

class C17:
    def __init__(self,registration,model,country):
        self.model = model
        self.registration = registration
        self.country = country

# Initialize Models

VUAUA = C17("C17","VUAUA","India")
VUAUB = C17("C17","VUAUB","India")
VUAUD = C17("C17","VUAUD","India")
VUAUH = C17("C17","VUAUH","India")
VUAUJ = C17("C17","VUAUJ","India")
VUAUK = C17("C17","VUAUK","India")
VUAUL = C17("C17","VUAUL","India")

