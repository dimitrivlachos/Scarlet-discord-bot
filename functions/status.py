import discord
import asyncio
import random
from utility.logger import logger
import utility.db_manager as db

async def update_status(client):
    # get a random status from the database
    new_status = db.get_random_response("status")
    # update the bot's status
    await client.change_presence(activity=discord.Game(name=new_status))
    logger.info(f"Updating status to '{new_status}'")

    # schedule the coroutine to run again after a random interval of time
    # Get a random number of seconds
    interval_seconds = get_random_time_interval(2, 4)
    # Get the event loop
    loop = asyncio.get_running_loop()
    # Schedule the coroutine to run again after interval_seconds
    loop.call_later(interval_seconds, asyncio.create_task, update_status(client))
    logger.info(f"Next status update in {interval_seconds} seconds")

def get_random_time_interval(min_hours=8, max_hours=24):
    '''
    Returns a random number of seconds between min_hours and max_hours
    
    Parameters:
        min_hours (int): The minimum number of hours
        max_hours (int): The maximum number of hours
        
    Returns:
        interval_seconds (int): The number of seconds
    '''
    # From hours to seconds
    min_seconds = min_hours * 60 * 60
    max_seconds = max_hours * 60 * 60
    # Get a random number of seconds
    interval_seconds = random.randint(min_seconds, max_seconds)
    
    return interval_seconds