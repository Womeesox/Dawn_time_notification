import os
import requests
from timezonefinder import TimezoneFinder
from time import sleep
from dotenv import load_dotenv
from pushbullet import PushBullet
from pytz import timezone

# load_dotenv()
# API_KEY = os.getenv("PUSHBULLET_API_KEY")
# pb = PushBullet(API_KEY)

#for cyvil dawn that is time when it's actually light outside
def get_dawn_time(lat, lng):
    url = "https://api.sunrise-sunset.org/json"

    params = {
        'lat': lat,
        'lng': lng,
        'formatted': 0  # 0 for ISO 8601 format, which includes the full date and time
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        dawn_time = data['results']['civil_twilight_begin']
        return dawn_time
    else:
        return None

#Warsaw, Poland    
latitude = 52.229675
longitude = 21.012230 

# print(type(get_dawn_time(latitude, longitude)))
print(get_time_zone(latitude, longitude))