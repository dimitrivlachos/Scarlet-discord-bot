'''
Basic discord bot that responds to messages with "Hello, World!"
'''

import discord
import requests
from discord.ext import commands

intents = discord.Intents.all()#discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# Reads token from binary file
with open("config/token.bin", "rb") as binary_file:
    token = binary_file.read().decode()

# Function to get weather from OpenWeatherMap API
def get_weather(city):
    # Get API key from binary file
    with open("config/open_weather.bin", "rb") as binary_file:
        api_key = binary_file.read().decode()

    # Get weather from API
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    response.raise_for_status()

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
    weather = f'{city.title()} Weather: {weather_desc}, {temp_celsius}°C, {wind_kmh} km/h'

    print(weather)

    return weather

# Prints a message to the console when the bot is ready
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# Responds to messages with "Hello, World!"
@client.event
async def on_message(message):
    print("Message received: " + message.content)

    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return
    
    response = 'Hello, World!'
    
    # If message has weather command, respond with weather
    if message.content.startswith('weather'):
        # Get the city name from the message
        city = message.content.split(' ')[1]
        # If there is no city name, return
        if not city:
            response = "I don't know what city you want the weather for!"

        else:
            # Get the weather from the API
            weather = get_weather(city)
            # Send the weather to the Discord channel
            await message.channel.send(weather)
            return

    # Send the response to the Discord channel
    await message.channel.send(response)

# Run the bot
client.run(token)