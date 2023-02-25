'''
Simple discord bot that responds to commands
'''

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import time

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

#client = commands.Bot(command_prefix = "!")

@client.event

async def on_ready():
    print(f'{client.user} has connected to Discord!')

# Reads token from binary file
with open("config/token.bin", "rb") as binary_file:
    token = binary_file.read().decode()

client.run(token)