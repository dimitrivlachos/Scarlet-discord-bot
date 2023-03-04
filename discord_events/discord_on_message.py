import discord
import asyncio
from utility.logger import logger
from functions import weather_api
from functions import wit_api

async def on_message(client, message):
    '''
    Handles messages sent to the bot
    
    Parameters:
        client (discord.Client): The bot client
        message (discord.Message): The message sent to the bot
        
    Returns:
        None
    '''
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return
    
    # Create a WitNlp object
    nlp = wit_api.WitNlp(message.content)
    logger.info(f"Created WitNlp: {nlp}")
   
    # Check if the message is a command for the bot
    if nlp.intent is None:
        return
    
    # At this point, we know the message is a command for the bot, so we create a task to parse the message
    task_response = asyncio.create_task(parse_message(nlp))

    # We also send a typing indicator so the user knows the bot is working on the response
    # This is done asynchronously, so the request can be processed while the typing indicator is being shown

    # Send typing indicator
    async with message.channel.typing():
        await asyncio.sleep(2)

    # Wait for the response to be created
    response = await task_response

    # Send the response
    await message.channel.send(response)

async def on_message_edit(client, before, after):
    # Ignore messages sent by the bot itself
    if before.author == client.user:
        return
    
    # Re-run the on_message function
    on_message(client, after)

async def parse_message(nlp):
    '''
    Parses the message and returns the response

    Parameters:
        nlp (WitNlp): The WitNlp object

    Returns:
        response (str): The response
    '''
    # Functions to handle each intent
    # The key is the intent name, and the value is the function to handle the intent
    # The function must take a WitNlp object as a parameter and return a string
    intent_functions = {
        'wit$get_weather': get_weather # This is the same as 'get_weather': get_weather
    }

    # Get the function to handle the intent
    # If the intent is not found, return a default response
    intent_function = intent_functions.get(nlp.intent, lambda: "I don't know how to do that yet :sob:")
    response = await intent_function(nlp)
    return await response


# Functions to handle each intent
async def get_weather(nlp):
    '''
    Returns the weather for the given location
    
    Parameters:
        location (str): The location to get the weather for
        
    Returns:
        weather (str): The weather for the given location
    '''
    weather = weather_api.get_weather(nlp.location)
    return weather