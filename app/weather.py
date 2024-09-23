import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str):
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }
    response = requests.get(WEATHER_API_URL, params=params)
    data = response.json()
    print (data)
    
    if response.status_code == 200:
        return {
            "weather_state": data["weather"][0]["main"],
            "temperature": data["main"]["temp"]
        }
    else:
        return None