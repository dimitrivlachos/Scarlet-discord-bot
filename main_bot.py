'''
Basic discord bot that responds to messages with "Hello, World!"
'''

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)

# Reads token from binary file
with open("config/token.bin", "rb") as binary_file:
    token = binary_file.read().decode()

# Prints a message to the console when the bot is ready
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# Responds to messages with "Hello, World!"
@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    response = 'Hello, World!'

    # Send the response to the Discord channel
    await message.channel.send(response)

# Run the bot
client.run(token)