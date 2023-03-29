import discord
import asyncio
from time import time
from utility.logger import logger

async def send_message(client, message, nlp, task, minimum_wait_time='auto', max_wait_time=1.5):
    '''
    Sends a message to the channel the message was sent in
    
    Parameters:
        client (discord.Client): The Discord client
        message (discord.Message): The message to send the response to
        nlp (WitNlp): The WitNlp object
        task (asyncio.Task): The task to get the response
        minimum_wait_time (float): The minimum time to wait before sending the response (default: 'auto')
        max_wait_time (float): The maximum time to wait before sending the response (default: 1.5)
        
    Returns:
        None'''
    logger.info(f"'Typing' message with task: {task}")
    # Create a task to get the response
    message_task = asyncio.create_task(task(nlp))

    # We also send a typing indicator so the user knows the bot is working on the response
    # This is done asynchronously, so the request can be processed while the typing indicator is being shown
    # Get the current time
    start_time = time()
    async with message.channel.typing():
        # Wait for the response to be created
        response = await message_task

        if minimum_wait_time == 'auto':
            # Calculate the minimum wait time based on the number of words in the response
            minimum_wait_time = typing_time(response)
            # If the minimum wait time is greater than the maximum wait time, set the minimum wait time to the maximum wait time
            if minimum_wait_time > max_wait_time:
                minimum_wait_time = max_wait_time

        # Calculate the time remaining
        time_remaining = minimum_wait_time - (time() - start_time)
        # If the time remaining is greater than 0, wait for the remaining time
        if time_remaining > 0:
            logger.info(f"'Typing' for {time_remaining} more seconds...")
            await asyncio.sleep(time_remaining)

    # Send the response
    await message.channel.send(response)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Helper functions

def count_words(text):
    '''
    Counts the number of words in the given text
    
    Parameters:
        text (str): The text to count the words in
        
    Returns:
        word_count (int): The number of words in the text
    '''
    # Split the text into words
    words = text.split()
    # Return the number of words
    return len(words)

def typing_time(text, wpm=75):
    '''
    Calculates the time it takes to type the given text
    
    Parameters:
        text (str): The text to calculate the time for
        wpm (int): The words per minute to type at (default: 75)
        
    Returns:
        typing_time (float): The time it takes to type the text
    '''
    # Get the number of words in the text
    word_count = count_words(text)
    # Calculate the time it takes to type the text
    typing_time = word_count / wpm * 60
    return typing_time