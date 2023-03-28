import discord
import asyncio
import re
from random import choice
from utility.logger import logger
from utility.tokens import BISCUIT_ID # Author's user ID
import utility.db_manager as db
from functions import weather_api, wit_api, dice

RESPONSE_DB = "db/responses.db"

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
    
    # Check if the message uses the bot's prefix
    # todo

    # Create a task to get the response
    process_nlp_response = asyncio.create_task(parse_nlp_task(client, message))

    # Wait for the message to be processed
    await process_nlp_response

async def on_message_edit(client, before, after):
    '''
    Handles messages edited by the user
    '''
    # Ignore messages sent by the bot itself
    if before.author == client.user:
        return
    
    # Re-run the on_message function
    on_message(client, after)

async def parse_nlp_task(client, message, confidence_threshold=0.8):
    '''
    Parses the message and returns the response

    Parameters:
        nlp (WitNlp): The WitNlp object

    Returns:
        response (str): The response
    '''
    # Create a WitNlp object
    nlp = wit_api.WitNlp(message.content)
    logger.info(f"Checked message from <{message.author}>: {nlp}")
    logger.info(f"Intents: {nlp.intents}")
   
    # Check if the message is a command for the bot
    # If it isn't, return
    if len(nlp.intents) == 0:
        logger.info("No intents found")
        return
    
    # Functions to handle each intent
    # The key is the intent name, and the value is the function to handle the intent
    # The function must take a WitNlp object as a parameter and return a string
    intent_functions = {
        'wit$get_weather': get_weather, # This is the same as 'get_weather': get_weather
        'roll_dice': roll_dice,
        'got_sick': respond_sick
    }

    # Check if the intent is above the confidence threshold
    intents = [intent for intent in nlp.intents if intent.confidence > confidence_threshold]

    # For each intent, get the function to handle the intent
    # If the intent is not found, return a default response
    for intent in intents:
        logger.info(f"Intent: {intent.name}")
        task = intent_functions.get(intent.name, lambda: "I don't know how to do that yet :sob:")
        await send_message(client, message, nlp, task)

    # Get the function to handle the intent
    # If the intent is not found, return a default response
    #intent_function = intent_functions.get(nlp.intent, lambda: "I don't know how to do that yet :sob:")
    #response = await intent_function(nlp)
    #return response


# Functions to handle each intent
async def get_weather(nlp):
    '''
    Returns the weather for the given location
    
    Parameters:
        location (str): The location to get the weather for
        
    Returns:
        weather (str): The weather for the given location
    '''
    # Check if there is a location entity
    if 'wit$location:location' not in nlp.entities:
        return "Where do you want the weather for?\nAsk me in a format like: 'what's the weather in London?' :see_no_evil:"

    # Get the location from the entities
    # This will only pull the first location mentioned, if there are multiple locations, the rest will be ignored
    location = nlp.entities['wit$location:location'][0]['resolved']['values'][0]['name']

    weather = await weather_api.get_weather(location)
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

async def respond_sick(nlp):
    '''
    Returns a response to the user being sick
    
    Parameters:
        nlp (WitNlp): The WitNlp object
        
    Returns:
        response (str): The response
    '''
    # Get a random response from a database
    response = db.get_random_response('sick_responses')

    return response

async def send_message(client, message, nlp, task):
    '''
    Sends a message to the channel the message was sent in
    
    Parameters:
        message (discord.Message): The message sent to the bot
        task (asyncio.Task): The task to get the response
        
    Returns:
        None'''
    # Create a task to get the response
    message_task = asyncio.create_task(task(nlp))

    # We also send a typing indicator so the user knows the bot is working on the response
    # This is done asynchronously, so the request can be processed while the typing indicator is being shown
    async with message.channel.typing():
        await asyncio.sleep(2)

    # Wait for the response to be created
    response = await message_task

    # Send the response
    await message.channel.send(response)