import discord
from logs.logger import logger

async def on_ready(client):
    logger.info(f'{client.user} has connected to Discord!')
    print(f'{client.user} has connected to Discord!')