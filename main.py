import discord
from discord.ext import commands
import asyncio
from utility.tokens import DISCORD_TOKEN
from utility.logger import logger
from discord_events import discord_on_ready
from discord_events import discord_on_message
from cogs.music_cog import music_cog

prefix = '!'

# Create the bot client
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)

# Handles the bot being ready
@bot.event
async def on_ready():
    await discord_on_ready.on_ready(bot)

# Handles messages sent to the bot
@bot.event
async def on_message(message):
    print(message.content)
    # Check if first character is the prefix
    if message.content[0] != prefix:
        await discord_on_message.on_message(bot, message)
    
    # Process commands
    await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):
    await discord_on_message.on_message_edit(bot, before, after)

async def main():
    async with bot:
        await bot.add_cog(music_cog(bot))
        await bot.start(DISCORD_TOKEN)

asyncio.run(main())