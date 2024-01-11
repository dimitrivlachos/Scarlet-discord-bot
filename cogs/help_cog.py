import discord
from discord.ext import commands
from utility.logger import logger
from utility.tokens import BISCUIT_ID

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.set_help_embed()
        self.set_music_embed()

    def set_help_embed(self):
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
        `{self.bot.command_prefix}join` - Joins the voice channel you are in
        `{self.bot.command_prefix}play` [query] - Plays / adds a song to the queue
        `{self.bot.command_prefix}add` [query] - Plays / adds a song to the queue
        `{self.bot.command_prefix}pause` - Pauses / Resumes the current song
        `{self.bot.command_prefix}resume` - Resumes the current song
        `{self.bot.command_prefix}skip` - Skips the current song
        `{self.bot.command_prefix}queue` [depth] - Displays the queue (depth optional)
        `{self.bot.command_prefix}clear` - Clears the current queue
        `{self.bot.command_prefix}stop` - Stops the current song, clears the queue and leaves
        `{self.bot.command_prefix}remove` [query] - Removes the specified song from the queue
        `{self.bot.command_prefix}move` [song] [position] - Moves a song to a new position in the queue
        `{self.bot.command_prefix}shuffle` - Shuffles the queue
        """
        self.help_embed.add_field(name="Music commands", value=music_commands, inline=False)

        # Add the help command to the embed
        self.help_embed.add_field(name=f"{self.bot.command_prefix}help", value=f"Displays this message. Or `{self.bot.command_prefix}help music` (`{self.bot.command_prefix}help m`) to show more detail on the music commands", inline=False)
    
    def set_music_embed(self):
        music_description = f"""
        Here are the commands you can use to control the music:
        """
        self.music_embed = discord.Embed(title="Music help", description=music_description, color=0x00ff00)

        self.music_embed.add_field(name=f"{self.bot.command_prefix}join ({self.bot.command_prefix}j)", value="Joins the voice channel you are in", inline=False)
        self.music_embed.add_field(name=f"{self.bot.command_prefix}play [query] ({self.bot.command_prefix}p {self.bot.command_prefix}playing {self.bot.command_prefix}a {self.bot.command_prefix}add)", value="Plays / adds a song to the queue", inline=False)
        self.music_embed.add_field(name=f"{self.bot.command_prefix}add [query] ({self.bot.command_prefix}p {self.bot.command_prefix}playing {self.bot.command_prefix}a {self.bot.command_prefix}add))", value="Plays / adds a song to the queue", inline=False)
        self.music_embed.add_field(name=f"{self.bot.command_prefix}pause", value="Pauses / Resumes the current song", inline=False)
        self.music_embed.add_field(name=f"{self.bot.command_prefix}resume ({self.bot.command_prefix}r)", value="Resumes the current song", inline=False)
        self.music_embed.add_field(name=f"{self.bot.command_prefix}skip ({self.bot.command_prefix}s)", value="Skips the current song", inline=False)
        self.music_embed.add_field(name=f"{self.bot.command_prefix}queue [depth] ({self.bot.command_prefix}q)", value="Displays the queue (depth optional)", inline=False)
        self.music_embed.add_field(name=f"{self.bot.command_prefix}clear ({self.bot.command_prefix}c {self.bot.command_prefix}bin {self.bot.command_prefix}empty)", value="Clears the current queue", inline=False)
        self.music_embed.add_field(name=f"{self.bot.command_prefix}stop ({self.bot.command_prefix}disconnect {self.bot.command_prefix}l {self.bot.command_prefix}d {self.bot.command_prefix}dc)", value="Stops the current song, clears the queue and leaves", inline=False)
        self.music_embed.add_field(name=f"{self.bot.command_prefix}remove [query] ({self.bot.command_prefix}rm)", value="Removes the specified song from the queue", inline=False)
        self.music_embed.add_field(name=f"{self.bot.command_prefix}move [song] [position] ({self.bot.command_prefix}mv)", value="Moves a song to a new position in the queue", inline=False)
        self.music_embed.add_field(name=f"{self.bot.command_prefix}shuffle ({self.bot.command_prefix}sh)", value="Shuffles the queue", inline=False)
    
    @commands.command(name='help', help="Displays all of my functions")
    async def help(self, ctx, *args):
        query = " ".join(args)
        if query == "music" or query == "m":
            logger.info(f"Sending music help message to <{ctx.author}>")
            await ctx.send(embed=self.music_embed)
        else:
            logger.info(f"Sending help message to <{ctx.author}>")
            await ctx.send(embed=self.help_embed)