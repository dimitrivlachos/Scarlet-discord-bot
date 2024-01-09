import discord
import asyncio
import re
from discord.ext import commands
from yt_dlp import YoutubeDL
from utility.logger import logger
from functions.send import send_message

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        #all the music related stuff
        self.is_playing = False
        self.is_paused = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio/best'}
        self.FFMPEG_OPTIONS = {
            'options': '-vn',
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
            }

        self.vc = None
        self.ytdl = YoutubeDL(self.YDL_OPTIONS)

    def parse_url(self, url):
        '''Extracts the relevant information from yotube the url using a regular expression
        
        Parameters:
            url (str): The url to parse
            
            Returns:
                urls (list): A list of urls
        '''
        logger.info(f"Parsing url: {url}")

        ids = []

        # Check if the url is a youtube url
        if "youtube.com/watch?" in url:
            exp = r"v=([0-9A-Za-z_-]+)"
            match = re.search(exp, url)
            if match:
                logger.info(f"Found url: {match.group(1)}")
                ids.append(match.group(1))
        
        # Check if the url is a youtube video url
        elif "youtu.be/" in url:
            exp = r"youtu.be/([0-9A-Za-z_-]+)"
            match = re.search(exp, url)
            if match:
                logger.info(f"Found url: {match.group(1)}")
                ids.append(match.group(1))

        # Check if the url is a youtube playlist url
        elif "youtube.com/playlist?" in url:
            exp = r"list=([0-9A-Za-z_-]+)"
            match = re.search(exp, url)
            if match:
                logger.info(f"Found playlist: {match.group(1)}")
                ids = self.get_playlist_urls(match.group(1))

        # Add youtube.com to the start of each url
        for i in range(0, len(ids)):
            # Check if the url already has youtube.com in it
            ids[i] = "https://www.youtube.com/watch?v=" + ids[i]

        return ids
    
    def get_playlist_urls(self, playlist_id):
        '''Gets the urls from a youtube playlist
        
        Parameters:
            playlist_id (str): The id of the playlist
            
        Returns:
            urls (list): A list of urls
        '''
        logger.info(f"Getting playlist urls for {playlist_id}")

        urls = []

        try:
            playlist_info = self.ytdl.extract_info(f"https://www.youtube.com/playlist?list={playlist_id}", download=False)
            
            if 'entries' in playlist_info:
                for video in playlist_info['entries']:
                    if 'webpage_url' in video:
                        urls.append(video['webpage_url'])

        except Exception as e:
            logger.error(f"Error getting playlist urls: {e}")

        logger.info(f"Found {len(urls)} urls")
        logger.info(f"Playlist urls: {urls}")

        # Extract the ids from the urls
        ids = []
        for url in urls:
            exp = r"v=([0-9A-Za-z_-]+)"
            match = re.search(exp, url)
            if match:
                ids.append(match.group(1))

        return ids

     #searching the item on youtube
    def search_yt(self, ctx, item):
        logger.info(f"Searching item: {item}")
        urls = self.parse_url(item)

        data_list = []

        # Check if the url is a playlist
        if len(urls) > 1:
            logger.info("Playlist detected")

        for url in urls:
            try:
                info = self.ytdl.extract_info(url, download=False)
            except Exception as e:
                logger.error(f"Error searching youtube: {e}")

            data = {'source': info['url'], 'title': info['title'], 'thumbnail': info['thumbnail'], 'duration': info['duration'], 'thumbnail': info['thumbnail']}
            data_list.append(data)

        # Check if data_list is empty
        if len(data_list) == 0:
            return None
        else:
            return data_list
    
    async def play_next(self):
        logger.info("Playing next song")

        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']

            #remove the first element as you are currently playing it
            self.music_queue.pop(0)
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(m_url, download=False))
            song = data['url']
            self.vc.play(discord.FFmpegPCMAudio(song, executable= "ffmpeg.exe", **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
        else:
            logger.info("play_next: No more songs in queue")
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self, ctx):
        logger.info("Playing music")

        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            #try to connect to voice channel if you are not already connected
            if self.vc == None or not self.vc.is_connected():
                logger.info("Connecting to voice channel")
                self.vc = await self.music_queue[0][1].connect()

                #in case we fail to connect
                if self.vc == None:
                    logger.error("Failed to connect to voice channel")
                    await send_message(ctx.channel, "I couldn't connect to the voice channel :sad:")
                    return
            else:
                logger.info("Moving to voice channel")
                await self.vc.move_to(self.music_queue[0][1])

            #remove the first element as you are currently playing it
            self.music_queue.pop(0)
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(m_url, download=False))
            song = data['url']
            self.vc.play(discord.FFmpegPCMAudio(song, executable= "ffmpeg.exe", **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))

        else:
            logger.info("play_music: No more songs in queue")
            self.is_playing = False

    @commands.command(name="play", aliases=["p","playing", "a", "add"], help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        
        logger.info(f"Attempting to add {query}")

        try:
            logger.info("Checking if user is in a voice channel")
            voice_channel = ctx.author.voice.channel
        except:
            logger.error("User not in a voice channel")
            await send_message(ctx.channel, "You need to be in a voice channel to use this command, how else am I supposed to play music for you?")
            return
        if self.is_paused:
            self.vc.resume()
        else:
            # Check if the message contains the word playlist
            if "playlist" in query:
                logger.info("Playlist detected")
                await send_message(ctx.channel, "I am downloading the playlist, this may take a little bit...", max_wait_time=1.5)

            songs = self.search_yt(ctx, query)

            if songs is None:
                await send_message(ctx.channel, "I couldn't download the song :pensive: Maybe the format isn't supported?") 
            else:
                embed = discord.Embed(title="Added to queue", color=discord.Color.red())
                # Loop through each song in songs
                for i, song in enumerate(songs):
                    # Check if the bot is already playing
                    if i < 5:
                        if self.is_playing:
                            embed.add_field(name=f"#{len(self.music_queue) + 2}", value=f"'{song['title']}'", inline=False)
                        else:
                            embed.add_field(name=f"#{len(self.music_queue) + 1}", value=f"'{song['title']}'", inline=False)
                    elif i == 5:
                        embed.add_field(name="...", value="There are more songs, but I'm not going to show them all :see_no_evil:", inline=False)

                    # Set the thumbnail, assuming the song dictionary has a 'thumbnail' key
                    embed.set_thumbnail(url=song['thumbnail'])

                    # Add the song to the music queue
                    self.music_queue.append([song, voice_channel])
                    
                    # Play music if the bot is not already playing
                    if not self.is_playing:
                        await self.play_music(ctx)

                # Delete the message that triggered the command
                await ctx.message.delete()
                
                # Send the embed
                await ctx.send(embed=embed)

    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, ctx, *args):
        logger.info("Pause called")
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command(name = "resume", aliases=["r"], help="Resumes playing with the discord bot")
    async def resume(self, ctx, *args):
        logger.info("Resume called")
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        logger.info("Skip called")
        if self.vc != None and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await self.play_music(ctx)

    @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx):
        logger.info("Queue requested")

        if len(self.music_queue) == 0:
            await send_message(ctx.channel, "There are no songs in the queue!")
            return

        embed = discord.Embed(title="Music Queue", color=discord.Color.red())
        
        for i, song_info in enumerate(self.music_queue):
            song_title = song_info[0]['title']
            embed.add_field(name=f"#{i + 1}", value=song_title, inline=False)

            if i == 5:
                embed.add_field(name="...", value="There are more songs, but I'm not going to show them all :see_no_evil:", inline=False)
                break

        await ctx.send(embed=embed)

    @commands.command(name="clear", aliases=["c", "bin", "empty"], help="Stops the music and clears the queue")
    async def clear(self, ctx):
        logger.info("Clear called")
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("```Music queue cleared```")

    @commands.command(name="stop", aliases=["disconnect", "l", "d"], help="Kick the bot from VC")
    async def dc(self, ctx):
        logger.info("Disconnect called")
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
    
    @commands.command(name="remove", help="Removes last song added to queue")
    async def re(self, ctx):
        logger.info("Remove called")
        self.music_queue.pop()
        await ctx.send("```last song removed```")