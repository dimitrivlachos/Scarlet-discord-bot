import discord
from functions import weather_api

async def on_message(client, message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return
    
    # Check if the bot is mentioned in the message
    if client.user in message.mentions:
        await message.channel.send("Hi! I'm a bot! I can only tell the weather for now. Try typing 'weather <city>'! :sunny:\n\nI'm still in development, so I'll be getting more features soon! :smile:")
    else:
        # Print message to console
        print("Message received: " + message.content)
        
        # If message has weather command, respond with weather
        if message.content.startswith('weather'):
            message_contents = message.content.split(' ')

            if len(message_contents) < 2:
                response = "I don't know what city you want the weather for!"

            else:
                # Get the city name from the message
                city = message_contents[1]
                # Get the weather from the API
                weather = weather_api.get_weather(city)
                # Send the weather to the Discord channel
                response = weather
            
            await message.channel.send(response)