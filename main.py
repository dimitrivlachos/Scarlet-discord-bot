import discord
from discord.ext import commands
import asyncio
from utility.tokens import DISCORD_TOKEN
from utility.logger import logger, logging
from discord_events import discord_on_ready
from discord_events import discord_on_message
from cogs.help_cog import help_cog
from cogs.music_cog import music_cog

logger.log(logging.INFO, "Starting bot...", extra={'colour': "\033[0;35m"})

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
    logger.info(f"Message from <{message.author}>: {message.content}")

    # Check if the message is a command (starts with the prefix)
    if message.content.startswith(prefix):
        # Process the command
        await bot.process_commands(message)
    else:
        # Handle non-command messages
        await discord_on_message.on_message(bot, message)

@bot.event
async def on_message_edit(before, after):
    await discord_on_message.on_message_edit(bot, before, after)

# Remove the default help command
bot.remove_command('help')

async def main():
    async with bot:
        await bot.add_cog(help_cog(bot))
        await bot.add_cog(music_cog(bot))
        await bot.start(DISCORD_TOKEN)

asyncio.run(main())