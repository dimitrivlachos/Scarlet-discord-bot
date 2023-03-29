import requests
from utility.tokens import WEATHER_API_KEY
from utility.logger import logger

# Function to get weather from OpenWeatherMap API
async def get_weather(city, retries=3):
    logger.info(f"Getting weather for: {city}")

    # Get weather from API
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}'

    # Make request
    for i in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            break
        except requests.exceptions.Timeout:
            logger.warning(f"Request timed out, retrying ({i+1}/{retries})")
            continue
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return None
    
    # Check if city was found
    # Not sure if this is necessary anymore after the above checking was added
    if response.status_code == 404:
        logger.warning(f"Couldn't find city: {city}")
        return None

    # Convert response to JSON
    weather_data = response.json()

    # Get weather description
    weather_desc = weather_data['weather'][0]['description']

    # Get temperature in Celsius
    temp = weather_data['main']['temp']
    temp_celsius = round(temp - 273.15)

    # Get wind speed in km/h
    wind = weather_data['wind']['speed']
    wind_kmh = round(wind * 3.6)

    # Format weather message
    weather = f'The weather in {city.title()} is: {weather_desc}, {temp_celsius}°C, with winds of {wind_kmh} km/h'
    logger.info(f"Weather received: {weather}")

    return weather