import os
import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Reads token from binary file
with open("config/token.bin", "rb") as binary_file:
    token = binary_file.read().decode()

# Reads OpenAI API key from binary file
with open("config/openai_api_key.bin", "rb") as binary_file:
    openai_api_key = binary_file.read().decode().strip()

# Define the ChatGPT API endpoint and headers
GPT_ENDPOINT = 'https://api.openai.com/v1/engines/davinci-codex/completions'
GPT_HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {openai_api_key}'
}

@bot.command()
async def chat(ctx, *, message: str):
    # Send the input message to the ChatGPT API
    print(f'Sending message "{message}" to ChatGPT API...')
    data = {
        'prompt': f'{message}\nAI:',
        'max_tokens': 50,
        'temperature': 0.7
    }
    response = requests.post(GPT_ENDPOINT, headers=GPT_HEADERS, json=data)
    json_response = response.json()
    # Send the response from ChatGPT to the Discord channel
    print(f'Received response from ChatGPT API: "{json_response["choices"][0]["text"].strip()}"')
    await ctx.send(json_response['choices'][0]['text'].strip())

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

bot.run(token)
