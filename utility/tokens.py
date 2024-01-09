from utility.logger import logger
'''
Import the tokens from the files in the config directory.
'''
logger.info("Reading tokens from binary files...")

global DISCORD_TOKEN
global WEATHER_API_KEY
global WIT_AI_TOKEN
global BISCUIT_ID

# Reads bot token from binary file
logger.info("Reading bot token...")
with open("config/token.bin", "rb") as binary_file:
    DISCORD_TOKEN = binary_file.read().decode()

# Reads OpenWeatherMap API key from binary file
logger.info("Reading OpenWeatherMap API key...")
with open("config/open_weather.bin", "rb") as binary_file:
    WEATHER_API_KEY = binary_file.read().decode()

# Reads Wit.ai access token from binary file
logger.info("Reading Wit.ai access token...")
with open("config/wit_ai.bin", "rb") as binary_file:
    WIT_AI_TOKEN = binary_file.read().decode()

# Reads the biscuit ID from binary file
logger.info("Reading Biscuit ID...")
with open("config/biscuit.bin", "rb") as binary_file:
    # The biscuit ID is stored as a string, so we need to convert it to an int
    BISCUIT_ID = int(binary_file.read().decode())