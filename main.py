import discord
from utility.tokens import DISCORD_TOKEN
from utility.logger import logger
from discord_events import discord_on_ready
from discord_events import discord_on_message

# Create the bot client
intents = discord.Intents.all()
#intents.members = True
client = discord.Client(intents=intents)

# Handles the bot being ready
@client.event
async def on_ready():
    await discord_on_ready.on_ready(client)

# Handles messages sent to the bot
@client.event
async def on_message(message):
    print(message.content)
    await discord_on_message.on_message(client, message)

@client.event
async def on_message_edit(before, after):
    await discord_on_message.on_message_edit(client, before, after)

# Run the bot
client.run(DISCORD_TOKEN)