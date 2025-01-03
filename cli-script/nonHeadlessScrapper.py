from playwright.sync_api import sync_playwright
import math

# Radius of the Earth in miles
R = 3959

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance in miles between two points
    on the Earth's surface given by their latitude and longitude.
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def is_within_radius(lat1, lon1, lat2, lon2, radius=100):
    """
    Check if the given latitude and longitude (lat2, lon2) are within
    the specified radius (default 100 miles) of the reference point (lat1, lon1).
    """
    distance = haversine(lat1, lon1, lat2, lon2)
    if distance <= radius:
        return True  # The location is within the radius
    else:
        return False  # The location is outside the radius


# Latitude and longitude of the city Vadodara
city_lat = 22.310696
city_lon = 73.192635    



aircraftReg = 'VUMAF'
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, timeout=60000)  # Timeout set to 60 seconds

 
     # headful mode (with browser UI)
    page = browser.new_page()
    page.goto(f"https://www.radarbox.com/data/flights/{aircraftReg}")
    page.wait_for_load_state('load')
    print(page.title())  # This will print the title of the page
    # latitude = page.locator('.sc-pbvqsk-0 btLBKZ').text_content().strip()
   # Assuming you have already fetched the latitude and longitude as strings

    target_lat_str = page.locator('div#title:has-text("Latitude")').locator('xpath=following-sibling::div[@id="value"]').text_content().strip()
    target_lon_str = page.locator('div#title:has-text("Longitude")').locator('xpath=following-sibling::div[@id="value"]').text_content().strip()

    target_lat = float(target_lat_str.replace("-", ""))
    target_lon = float(target_lon_str.replace("-", ""))
    

    print(f"Latitude: {target_lon}")

    if is_within_radius(city_lat, city_lon, target_lat, target_lon):
     print(f"{aircraftReg} is within 100 miles of Vadodara (Lat : {target_lat} , long {target_lon}).")
    else:
     print(f"{aircraftReg} is NOT within 100 miles of the city.")

    


    browser.close()

