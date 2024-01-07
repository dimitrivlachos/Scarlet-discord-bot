import discord
from discord.ext import commands
import asyncio
from utility.tokens import DISCORD_TOKEN
from utility.logger import logger
from discord_events import discord_on_ready
from discord_events import discord_on_message
from cogs.music_cog import music_cog

# Create the bot client
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='&', intents=intents)

# Handles the bot being ready
@bot.event
async def on_ready():
    await discord_on_ready.on_ready(bot)

# Handles messages sent to the bot
@bot.event
async def on_message(message):
    print("Message received")
    print(message.content)
    print("Message content printed")
    await discord_on_message.on_message(bot, message)
    print("Message processed")
    await bot.process_commands(message)
    print("Message commands processed")

@bot.event
async def on_message_edit(before, after):
    await discord_on_message.on_message_edit(bot, before, after)

# Run the bot
#client.run(DISCORD_TOKEN)

async def main():
    async with bot:
        await bot.add_cog(music_cog(bot))
        await bot.start(DISCORD_TOKEN)

asyncio.run(main())