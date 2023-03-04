'''
Import the tokens from the files in the config directory.
'''

# Reads bot token from binary file
with open("config/token.bin", "rb") as binary_file:
    global DISCORD_TOKEN 
    DISCORD_TOKEN = binary_file.read().decode()

# Reads OpenWeatherMap API key from binary file
with open("config/open_weather.bin", "rb") as binary_file:
    global WEATHER_API_KEY 
    WEATHER_API_KEY = binary_file.read().decode()

# Reads Wit.ai access token from binary file
with open("config/wit_ai.bin", "rb") as binary_file:
    global WIT_AI_TOKEN 
    WIT_AI_TOKEN = binary_file.read().decode()