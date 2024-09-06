import os
import requests

from dotenv import load_dotenv
from json import load as json_load, JSONDecodeError

from time import sleep

from datetime import datetime, timedelta
from timezonefinder import TimezoneFinder
from time import sleep
from pytz import utc, timezone

from pushbullet import Pushbullet

load_dotenv()
API_KEY = os.getenv("PUSHBULLET_API_KEY")
pb = Pushbullet(API_KEY)

try:
    config_file_path = "config.json"
    with open(config_file_path, "r") as file:
        config = json_load(file)

    latitude = config["latitude"]
    longitude = config["longitude"]

    if latitude is None or longitude is None:
        raise ValueError("Latitude and longitude must be specified in the config file.")
except FileNotFoundError:
    print(f"Error: The file {config_file_path} does not exist.")
except JSONDecodeError:
    print("Error: The config file is not a valid JSON.")
except ValueError as e:
    print(f"Error: {e}")

tf = TimezoneFinder()
local_timezone = timezone(tf.timezone_at(lat=latitude, lng=longitude))


#for civil dawn that is time when it's actually light outside
def get_dawn_time(lat, lng):
    url = "https://api.sunrise-sunset.org/json"

    params = {
        "lat": lat,
        "lng": lng,
        "formatted": 0  # 0 for ISO 8601 format, which includes the full date and time
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        dawn_time = data["results"]["civil_twilight_begin"]
        
        utc_time = datetime.fromisoformat(dawn_time.replace("Z", "+00:00")) # parse to datetime object
        local_time = utc_time.astimezone(local_timezone)


        return local_time
    else:
        return None  

while(True):
    now = datetime.now()
    dawn_time = get_dawn_time(latitude, longitude)

    if dawn_time < now:
        dawn_time += timedelta(days=1)

    time_diff = (dawn_time - now).total_seconds()

    sleep(time_diff)
    push = pb.push_note("It's light outside! 🥳", "Time to get some sunlight 🌞")