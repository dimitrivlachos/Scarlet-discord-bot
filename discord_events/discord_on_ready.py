import discord
import asyncio
from utility.logger import logger
from functions.status import update_status

async def on_ready(client):
    logger.info(f'{client.user} has connected to Discord!')
    asyncio.create_task(update_status(client))  # start the status update coroutine using create_task()