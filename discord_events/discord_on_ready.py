import discord
from utility.logger import logger

async def on_ready(client):
    logger.info(f'{client.user} has connected to Discord!')