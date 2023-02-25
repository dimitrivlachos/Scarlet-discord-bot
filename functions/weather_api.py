import requests

# Function to get weather from OpenWeatherMap API
def get_weather(city):
    # Get API key from binary file
    with open("config/open_weather.bin", "rb") as binary_file:
        api_key = binary_file.read().decode()

    # Get weather from API
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    
    # Check if city was found
    if response.status_code == 404:
        return "I couldn't find that city! :sob:"

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
    weather = f'{city.title()} Weather: {weather_desc}, {temp_celsius}°C, with winds of {wind_kmh} km/h'

    print(weather)

    return weather