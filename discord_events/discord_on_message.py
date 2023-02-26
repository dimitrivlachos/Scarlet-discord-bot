import discord
import asyncio
from logs.logger import logger
from functions import weather_api

async def on_message(client, message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return
    
    # Print the message to the console
    logger.info(f"Received message: {message.content}")
    print("Received message:", message.content)

    # Correct old command
    # TO REMOVE SOON
    if message.content.startswith('weather'):
        # Send typing indicator
        async with message.channel.typing():
            await asyncio.sleep(2)
        await message.channel.send(f"I've changed my prefix to '{client.user.mention}!' :smile: \n\nTry @'ing me by typing '{client.user.mention} weather <city>'! :sunny:")
        return
    
    # Ignore messages that don't mention the bot
    if client.user not in message.mentions:
        return
    
    # At this point, we know the message is a command for the bot
    # and that the bot will respond to it. So, we can send a typing indicator
    # Send typing indicator
    async with message.channel.typing():
        await asyncio.sleep(2)

    # Parse the message
    await parse_message(client, message)

async def parse_message(client, message):
    # Split the message into a list of words
    message_contents = message.content.split(' ')

    # Convert all the words to lowercase
    message_contents = [word.lower() for word in message_contents]

    # Print the message contents to the console
    print(message_contents)
    

    if len(message_contents) < 2:
        await message.channel.send(f"Hi! I'm a bot! I can only tell the weather for now. Try typing '{client.user.mention} weather <city>'! :sunny:\n\nI'm still in development, so I'll be getting more features soon! :smile:")
        return
    
    # Check if the message starts with the bot's name
    if message_contents[0] != f'<@{client.user.id}>':
        await message.channel.send(f"Please start the message with my name! :smile: \n\nExample: '{client.user.mention} weather <city>'\nOther commands will be added soon! :smile:")
        return
    
    message_contents = message_contents[1:]
    
    # Check if the message is a weather request
    if message_contents[0] == 'weather':
        # Check if the user specified a city
        if len(message_contents) < 2:
            await message.channel.send("I don't know what city you want the weather for!")
            return
        
        # Get the city name from the message
        city = message_contents[1]
        # Get the weather from the API
        weather = await weather_api.get_weather(city)
        # Send the weather to the Discord channel
        response = weather
        # Send the response to the Discord channel
        await message.channel.send(response)
        return
    
    await message.channel.send(f"I don't know what you want me to do! :sweat_smile: \n\nTry typing '{client.user.mention} weather <city>'! :sunny:\n\nI'm still in development, so I'll be getting more features soon! :smile:")