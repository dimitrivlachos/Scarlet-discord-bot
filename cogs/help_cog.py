import discord
from discord.ext import commands
from utility.logger import logger
from utility.tokens import BISCUIT_ID

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_embed = self.set_embed()

    def set_embed(self):
        help_description = f"""
        Hi! I am a bot created by <@!{BISCUIT_ID}>.
        I can do a few things, but I am still in development, so be kind!

        I am a natural language processing bot, Which means that you can ask me questions in a natural way.
        For example, you can ask me what the weather is like in London, and I'll tell you!

        I can also play music! Check out the music commands below to see what I can do.
        """
        self.help_embed = discord.Embed(title="Help menu", description=help_description, color=0x00ff00)

        # Natural language commands
        nlp_description = f"""
        I can tell you the weather in any city in the world! :sunny:
        Ask me: "what's the weather in London?" or "What's it like in Paris?"
        
        You can also ask me to roll a dice for you! :game_die:
        Say: "roll 2d20" and I'll work it out!

        I used to be able to do more, but <@!{BISCUIT_ID}> said I was getting annoying :slight_frown:
        But I'm sure I'll be able to do more soon! :smile:
        """
        self.help_embed.add_field(name="Natural language capability", value=nlp_description, inline=False)

        # Music commands
        music_commands = f"""
        {self.bot.command_prefix}play [query] - Plays / adds a song to the queue
        {self.bot.command_prefix}add [query] - Plays / adds a song to the queue
        {self.bot.command_prefix}pause - Pauses / Resumes the current song
        {self.bot.command_prefix}resume - Resumes the current song
        {self.bot.command_prefix}skip - Skips the current song
        {self.bot.command_prefix}queue - Displays the current queue
        {self.bot.command_prefix}clear - Clears the current queue
        {self.bot.command_prefix}stop - Stops the current song and clears the queue
        {self.bot.command_prefix}remove - Removes the last song from the queue
        """
        self.help_embed.add_field(name="Music commands", value=music_commands, inline=False)

        # Add the help command to the embed
        self.help_embed.add_field(name="!help", value="Displays this message", inline=False)

        return self.help_embed
    
    @commands.command(name='help', help="Displays all of my functions")
    async def help(self, ctx):
        logger.info(f"Sending help message to <{ctx.author}>")
        await ctx.send(embed=self.help_embed)