import aiohttp
from functions.unit_conversion import *
from utility.tokens import WEATHER_API_KEY
from utility.logger import logger

# Function to get weather from OpenWeatherMap API
async def get_weather(city, retries=3):
    logger.info(f"Getting weather for: {city}")

    # Get weather from API
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}'

    # Create an aiohttp session
    async with aiohttp.ClientSession() as session:
        for i in range(retries):
            try:
                async with session.get(url) as response:
                    # Raise an exception for HTTP error statuses
                    response.raise_for_status()

                    # Convert response to JSON
                    weather_data = await response.json()

                    # Process the data (same as before)
                    weather_desc = weather_data['weather'][0]['description']
                    temp = weather_data['main']['temp']
                    temp_celsius = kelvin_to_celsius(temp)
                    temp_fahrenheit = kelvin_to_fahrenheit(temp)
                    wind = weather_data['wind']['speed']
                    wind_kmh = metres_per_sec_to_kmh(wind)
                    wind_mph = metres_per_sec_to_mph(wind)

                    # Format weather message
                    weather = f'The weather in {city.title()} is: {weather_desc}, {temp_celsius}°C ({temp_fahrenheit}°F), with winds of {wind_kmh} km/h ({wind_mph} mph)'
                    logger.info(f"Weather received: {weather}")

                    return weather
            except aiohttp.ClientError as e:
                if i < retries - 1:
                    logger.warning(f"Request failed, retrying ({i+1}/{retries})")
                    continue
                else:
                    logger.error(f"Request error: {e}")
                    return None
                
        logger.warning(f"Request failed after {retries} retries")
