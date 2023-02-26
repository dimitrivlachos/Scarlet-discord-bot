import discord
from utility.tokens import discord_token
from utility.logger import logger
from discord_events import discord_on_ready
from discord_events import discord_on_message

# Create the bot client
intents = discord.Intents.all()
#intents.members = True
client = discord.Client(intents=intents)

# Prints a message to the console when the bot is ready
@client.event
async def on_ready():
    await discord_on_ready.on_ready(client)

# Responds to messages with "Hello, World!" when mentioned
@client.event
async def on_message(message):
    await discord_on_message.on_message(client, message)

# Run the bot
client.run(discord_token)