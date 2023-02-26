'''
Import the tokens from the files in the config directory.
'''

# Reads bot token from binary file
with open("config/token.bin", "rb") as binary_file:
    global discord_token 
    discord_token = binary_file.read().decode()

# Reads OpenWeatherMap API key from binary file
with open("config/open_weather.bin", "rb") as binary_file:
    global weather_api_key 
    weather_api_key = binary_file.read().decode()