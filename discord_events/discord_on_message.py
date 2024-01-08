import discord
import asyncio
import re
from utility.logger import logger
# import utility.db_manager as db
from functions import weather_api, wit_api, dice
from functions.send import send_message

async def on_message(bot, message):
    '''
    Handles messages sent to the bot
    
    Parameters:
        client (discord.Client): The bot client
        message (discord.Message): The message sent to the bot
        
    Returns:
        None
    '''
    # Ignore messages sent by the bot itself
    if message.author == bot.user:
        return
    
    # Ignore messages sent by other bots
    if message.author.bot:
        return

    # Create a task to get the response
    process_nlp_response = asyncio.create_task(parse_nlp_task(bot, message))

    # Wait for the message to be processed
    await process_nlp_response

async def on_message_edit(bot, before, after):
    '''
    Handles messages edited by the user
    '''
    # Ignore messages sent by the bot itself
    if before.author == bot.user:
        return
    
    # Re-run the on_message function
    await on_message(bot, after)

async def parse_nlp_task(bot, message, confidence_threshold=0.8):
    '''
    Parses the message and returns the response

    Parameters:
        nlp (WitNlp): The WitNlp object

    Returns:
        response (str): The response
    '''
    # Remove mentions from the message using a regex
    msg = re.sub(r'<@!?\d+>', '', message.content)

    # Check if the message is empty or only contains whitespace
    if msg.isspace() or len(msg) == 0:
        logger.info("Message is empty or only contains whitespace")
        return

    # Create a WitNlp object
    nlp = wit_api.WitNlp(msg)
    logger.info(f"Checked message from <{message.author}>: {nlp}")
   
    # Check if the message is a command for the bot
    # If it isn't, return
    if len(nlp.intents) == 0:
        logger.info("No intents found")
        return
    else:
        logger.info(f"Intents: {nlp.intents}")
    
    # Functions to handle each intent
    # The key is the intent name, and the value is the function to handle the intent
    # The function must take a WitNlp object as a parameter and return a string
    intent_config = {
        'wit$get_weather': {
            'function': get_weather,
            'max_typing_time': 1.5
        },
        'roll_dice': {
            'function': roll_dice,
            'max_typing_time': 0.5
        }
    }

    # Check if the intent is above the confidence threshold
    intents = [intent for intent in nlp.intents if intent.confidence > confidence_threshold]

    # For each intent, get the function to handle the intent
    # If the intent is not found, return a default response
    for intent in intents:
        logger.info(f"Intent: {intent.name}")
        # Get the function and max typing time for the intent
        intent_config_data = intent_config.get(intent.name, {'function': lambda: "I don't know how to do that yet :sob:", 'max_typing_time': 3})
        task = intent_config_data['function']
        max_typing_time = intent_config_data['max_typing_time']
        # Run the function
        await send_message(bot, message, nlp, task, max_wait_time=max_typing_time)



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
    #location = nlp.entities['wit$location:location'][0]['resolved']['values'][0]['name']
    location = nlp.entities['wit$location:location'][0]['body']

    weather = await weather_api.get_weather(location)

    if weather is None:
        return f"I couldn't find the weather for {location} :sob: are you sure that's a real place?"

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

