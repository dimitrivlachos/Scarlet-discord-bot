import discord
import asyncio
import re
from random import choice
from utility.logger import logger
from utility.tokens import BISCUIT_ID
from functions import weather_api, wit_api, dice

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
    logger.info(f"Checked message: {nlp}")
   
    # Check if the message is a command for the bot
    # If it isn't, return
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
    '''
    Handles messages edited by the user
    '''
    # Ignore messages sent by the bot itself
    if before.author == client.user:
        return
    
    # Re-run the on_message function
    on_message(client, after)

async def send_message(channel_id, message):
    '''
    Sends a message to a channel
    
    Parameters:
        client (discord.Client): The bot client
        channel_id (int): The ID of the channel to send the message to
        message (str): The message to send
        
    Returns:
        None
    '''
    channel = client.get_channel(channel_id)
    await channel.send()

async def parse_message(nlp, confidence_threshold=0.8):
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
        'wit$get_weather': get_weather, # This is the same as 'get_weather': get_weather
        'roll_dice': roll_dice
    }

    intents = nlp.intents

    for intent in intents:
        if intent.confidence > confidence_threshold:
            

    # Get the function to handle the intent
    # If the intent is not found, return a default response
    intent_function = intent_functions.get(nlp.intent, lambda: "I don't know how to do that yet :sob:")
    response = await intent_function(nlp)
    return response


# Functions to handle each intent
async def get_weather(nlp):
    '''
    Returns the weather for the given location
    
    Parameters:
        location (str): The location to get the weather for
        
    Returns:
        weather (str): The weather for the given location
    '''
    weather = await weather_api.get_weather(nlp.location)
    return weather

async def roll_dice(nlp):
    '''
    Rolls dice and returns the result
    
    Parameters:
        nlp (WitNlp): The WitNlp object
        
    Returns:
        result (str): The result of the dice roll
    '''
    # Get the number of dice and the number of sides
    match = re.search(r'(\d+)d(\d+)', nlp.text)

    if match is None:
        return "What dice do you want me to roll?\nAsk me to roll dice in a format like: 'roll 2d6' :see_no_evil:"
    
    # Check if there were two groups
    #if len(match.groups()) != 2:
        #return "Ask me to roll dice in the format 'roll 2d6'"
    
    number_of_dice = int(match.group(1))
    number_of_sides = int(match.group(2))
    
    roll_results = dice.roll_dice(number_of_dice, number_of_sides)
    
    # Create the response
    result = f"Rolling {number_of_dice}d{number_of_sides}\n{roll_results} = {sum(roll_results)}"

    return result