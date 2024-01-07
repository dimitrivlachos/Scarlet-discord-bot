'''
Import the tokens from the files in the config directory.
'''
global BISCUIT_ID
global BOT_ID
global DISCORD_TOKEN
global WEATHER_API_KEY
global WIT_AI_TOKEN

#BOT_ID = 1078849300882280468 # This is unecessary as the bot can get its own ID by using client.user.id

# Reads bot token from binary file
with open("config/token.bin", "rb") as binary_file:
    DISCORD_TOKEN = binary_file.read().decode()

# Reads OpenWeatherMap API key from binary file
with open("config/open_weather.bin", "rb") as binary_file:
    WEATHER_API_KEY = binary_file.read().decode()

# Reads Wit.ai access token from binary file
with open("config/wit_ai.bin", "rb") as binary_file:
    WIT_AI_TOKEN = binary_file.read().decode()