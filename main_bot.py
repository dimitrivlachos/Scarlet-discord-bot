import discord
from logs.logger import logger
from discord_events import discord_on_ready
from discord_events import discord_on_message

# Create the bot client
intents = discord.Intents.all()
#intents.members = True
client = discord.Client(intents=intents)

# Reads token from binary file
with open("config/token.bin", "rb") as binary_file:
    token = binary_file.read().decode()

# Prints a message to the console when the bot is ready
@client.event
async def on_ready():
    await discord_on_ready.on_ready(client)

# Responds to messages with "Hello, World!" when mentioned
@client.event
async def on_message(message):
    await discord_on_message.on_message(client, message)

# Run the bot
client.run(token)