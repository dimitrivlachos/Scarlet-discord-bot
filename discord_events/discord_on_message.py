import discord
from functions import weather_api

async def on_message(client, message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return
    
    # Print the message to the console
    print(message.content)
    
    # Ignore messages that don't mention the bot
    if client.user not in message.mentions:
        return

    # Check if first word is bot's name
    message_contents = message.content.split(' ')

    print(message_contents)

    if len(message_contents) < 2:
        await message.channel.send("Hi! I'm a bot! I can only tell the weather for now. Try typing 'weather <city>'! :sunny:\n\nI'm still in development, so I'll be getting more features soon! :smile:")
        return
    
    # Check if the message starts with the bot's name
    if message_contents[0] != f'<@{client.user.id}>':
        await message.channel.send("Please start the message with my name! :smile: \n\nExample: @WeatherBot weather <city>\nOther commands will be added soon! :smile:")
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
        weather = weather_api.get_weather(city)
        # Send the weather to the Discord channel
        response = weather
        # Send the response to the Discord channel
        await message.channel.send(response)
        return