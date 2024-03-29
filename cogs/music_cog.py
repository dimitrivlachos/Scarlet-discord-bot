import discord
import asyncio
import random
import re
from discord.ext import commands
from yt_dlp import YoutubeDL
from utility.logger import logger
from utility.formatting import seconds_to_formatted_time
from functions.send import send_message
from concurrent.futures import ThreadPoolExecutor

class song_data:
    '''
    A class for storing song data
    '''
    def __init__(self, source, title, thumbnail, duration):
        self.source = source
        self.title = title
        self.thumbnail = thumbnail
        self.duration = duration

class music_cog(commands.Cog):
    '''
    A cog for playing music
    '''
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.queue = []

        self.YDL_OPTIONS = {'format': 'bestaudio/best'}
        self.FFMPEG_OPTIONS = {
            'options': '-vn',
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
            }
        
        self.vc = None
        self.ytdl = YoutubeDL(self.YDL_OPTIONS)

        # Create a thread pool executor for multithreading
        self.executor = ThreadPoolExecutor(max_workers=10)

    # # # # # # # # # # # # # # #
    #        Functions         

    def create_embed(self, title, songs, colour=discord.Colour.red(), limit=5):
        '''
        Creates an embed for the songs

        Parameters:
            songs (list): A list of song_data objects

        Returns:
            embed (discord.Embed): The embed
        '''
        logger.info(f"Creating embed for \"{title}\"")
        embed = discord.Embed(title=title, colour=colour)

        for i, song in enumerate(songs): # Start at 1 to avoid 0th song
            logger.info(f"Adding song to embed: {song.title}")
            if i < limit:
                duration = seconds_to_formatted_time(song.duration)
                embed.add_field(name=f"#{i+1}", value=f"{song.title} - {duration}", inline=False)
                embed.set_thumbnail(url=song.thumbnail)
            elif i == limit:
                embed.add_field(name="And more!", value="I won't show you *all* of them here :see_no_evil:", inline=False)
                break
        
        return embed
    
    # # # # # # # # # # # # # # #
    #      Async functions

    async def parse_url(self, url):
        '''
        Parses the URL and returns the video IDs

        Parameters:
            url (str): The URL to parse

        Returns:
            urls (list): A list of video URLs
        '''
        logger.info(f"Parsing URL: {url}")
        ids = await self.extract_ids(url)
        urls = ["https://www.youtube.com/watch?v=" + id for id in ids]
        print(f"URL list: {urls}")
        return urls
    
    async def extract_ids(self, url):
        '''
        Extracts the video IDs from the URL

        Parameters:
            url (str): The URL to parse

        Returns:
            ids (list): The video IDs
        '''
        patterns = {
            "youtube.com/watch?": r"v=([0-9A-Za-z_-]+)",
            "youtu.be/": r"youtu.be/([0-9A-Za-z_-]+)",
            "youtube.com/playlist?": r"list=([0-9A-Za-z_-]+)"
        }

        for key, pattern in patterns.items():
            if key in url:
                match = re.search(pattern, url)
                if match:
                    logger.info(f"Found URL: {match.group(1)}")
                    if key == "youtube.com/playlist?":
                        playlist_urls = await self.get_playlist_urls(match.group(1))
                        playlist_ids = [id[0] for id in await asyncio.gather(*(self.extract_ids(url) for url in playlist_urls))]
                        return playlist_ids
                    return [match.group(1)]

        logger.warning(f"No valid YouTube URL found in: {url}")
        return []
    
    async def get_playlist_urls(self, playlist_id):
        '''
        Gets the URLs for the videos in the playlist asynchronously

        Parameters:
            playlist_id (str): The playlist ID

        Returns:
            urls (list): A list of video URLs
        '''
        logger.info(f"Getting playlist URLs for {playlist_id}")
        try:
            loop = asyncio.get_event_loop()
            # Run the blocking call in a separate thread
            playlist_info = await loop.run_in_executor(self.executor, lambda: self.ytdl.extract_info(f"https://www.youtube.com/playlist?list={playlist_id}", download=False))
            return [video['webpage_url'] for video in playlist_info['entries'] if 'webpage_url' in video]
        except Exception as e:
            logger.error(f"Error getting playlist URLs: {e}")
            return []
    
    async def add_to_queue(self, item):
        '''
        Adds the item to the queue asynchronously

        Parameters:
            item (str): The item to add

        Returns:
            songs (list): A list of song_data objects
        '''
        logger.info(f"Adding to queue: {item}")
        songs = await self.search_yt_async(item)  # Await the asynchronous function
        self.queue.extend(songs)  # Extend the queue with the new songs
        return songs

    async def search_yt_async(self, item):
        '''
        Searches YouTube for the item and returns the data asynchronously using multithreading

        Parameters:
            item (str): The item to search for

        Returns:
            song_list (list): A list of song_data objects
        '''
        logger.info(f"Searching YouTube for: {item}")
        urls = await self.parse_url(item)
        song_list = []
        loop = asyncio.get_event_loop()

        # Run the blocking call in a separate thread
        logger.info("Running blocking call in separate thread", extra={'colour': "\033[0;35m", 'bold': True})
        futures = []
        for url in urls:
            # Schedule the synchronous function to run in a separate thread
            future = loop.run_in_executor(self.executor, self.ytdl.extract_info, url, False)
            futures.append(future)

        for future in asyncio.as_completed(futures):
            try:
                info = await future
                song = song_data(info['url'], info['title'], info['thumbnail'], info['duration'])
                song_list.append(song)
            except Exception as e:
                logger.error(f"Error searching YouTube: {e}")

        if not song_list:
            logger.warning(f"No data found for item: {item}")

        return song_list
    
    async def play_next(self):
        '''
        Plays the next song in the queue
        '''
        logger.info("Playing next song")
        try:
            if len(self.queue) > 0:
                # Get the next song in the queue
                song = self.queue.pop(0)
                logger.info(f"Playing song: {song.title}")

                # Play the song
                self.vc.play(discord.FFmpegPCMAudio(song.source, **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
                
                self.is_playing = True
                self.is_paused = False
            else:
                # No more songs in the queue
                logger.info("No more songs in the queue")
                self.is_playing = False
                self.is_paused = False
                await self.vc.disconnect()
                self.vc = None
        except Exception as e:
            logger.error(f"Error playing next song: {e}")
            self.is_playing = False
            self.is_paused = False
            await self.vc.disconnect()
            self.vc = None
    
    async def join_voice_channel(self, channel):
        '''
        Joins a voice channel
        
        Parameters:
            ctx (discord.ext.commands.Context): The context of the command
            channel (discord.VoiceChannel): The voice channel to join
            
        Returns:
            bool: True if successful, False otherwise
        '''
        if channel is None:
            logger.error("Channel is None")
            return False
        
        # Check if the bot is already in a voice channel
        if self.vc is None:
            logger.info(f"Attemtping to join voice channel: {channel.name}")
            # Connect to the voice channel
            self.vc = await channel.connect()

            if self.vc is None:
                logger.error("Failed to connect to voice channel")
                return False
            else:
                logger.info("Successfully connected to voice channel")
        elif self.vc == channel:
            # Already in the voice channel, do nothing
            pass
        else:
            # Move to the voice channel
            logger.info(f"Moving to voice channel: {channel.name}")
            await self.vc.move_to(channel)

        return True

    # # # # # # # # # # # # # # #
    #          Commands         

    @commands.command(name='join', help='Joins a voice channel', aliases=['j'])
    async def join(self, ctx, *args):
        try:
            await self.join_voice_channel(ctx.author.voice.channel)
        except Exception as e:
            logger.error(f"Error joining voice channel: {e}")
            await send_message(ctx.channel, "You need to be in a voice channel to use this command :slight_frown:")

    @commands.command(name="play", aliases=["p","playing", "a", "add"], help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        logger.info(f"Play called on: {query}")

        # Check if the bot is connected to a voice channel
        if self.vc is None:
            # Call join command
            await self.join(ctx, args)
        elif ctx.author.voice.channel is not None and self.vc.channel != ctx.author.voice.channel:
            await send_message(ctx.channel, "I don't we're in the same channel :thinking: you can use ```!join``` to call me over")

        # If the bot is paused, just resume
        if self.is_paused:
            self.vc.resume()
            return
        
        # Otherwise, add the song to the queue

        # Check if the query is a playlist and inform the user
        if "playlist" in query:
            logger.info("Playlist detected")
            download_notification = await send_message(ctx.channel, "Downloading playlist... :hourglass_flowing_sand: This could take a while!", max_wait_time=0.5)
        
        # Add the song to the queue
        new_songs = await self.add_to_queue(query)

        # Wait for the download notification to finish
        if "download_notification" in locals():
            logger.info("Deleting download notification")
            await download_notification.delete()

        # Check if any new songs were added and inform the user
        if new_songs:
            logger.info("New songs added")
            embed = self.create_embed("Added to queue", new_songs, colour=discord.Colour.green())
            await ctx.channel.send(embed=embed)
            if not self.is_playing:
                logger.info("Starting playback")
                await self.play_next()
            # Delete the command message
            await ctx.message.delete()
        else:
            logger.warning("No new songs added")
            await send_message(ctx.channel, "I couldn't find that song :sob:")

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
    async def queue(self, ctx, *args):
        logger.info("Queue called")
        query = " ".join(args)

        if len(self.queue) == 0:
            await send_message(ctx.channel, "No songs in queue")
        else:
            if query == "": # If no depth specified, use default
                embed = self.create_embed("Queue", self.queue)
            else: # Otherwise, use the specified depth
                try:
                    depth = int(query)
                except ValueError:
                    await send_message(ctx.channel, "You need to use a number to specify the depth :see_no_evil:")
                    return
                if depth < 1:
                    await send_message(ctx.channel, "I can't show you less than 1 song :sweat_smile:")
                    return
                elif depth > 25:
                    depth = 25
                    await send_message(ctx.channel, "That's too many songs!")

                if depth > len(self.queue):
                    await send_message(ctx.channel, "I can't show you more songs than there are in the queue :sweat_smile:")
                    depth = len(self.queue)

                embed = self.create_embed("Queue", self.queue, limit=depth)
            
            await ctx.channel.send(embed=embed)

    @commands.command(name="clear", aliases=["c", "bin", "empty"], help="Stops the music and clears the queue")
    async def clear(self, ctx):
        logger.info("Clear called")
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.queue = []
        await send_message(ctx.channel, "Queue cleared")

    @commands.command(name="stop", aliases=["disconnect", "l", "d", "dc"], help="Kick the bot from VC")
    async def dc(self, ctx):
        logger.info("Disconnecting called")
        self.clear(ctx)
        await self.vc.disconnect()

    @commands.command(name="remove", aliases=["rm"], help="Removes a song from the queue")
    async def remove(self, ctx, *args):
        logger.info("Remove called")
        if len(args) == 0:
            await send_message(ctx.channel, "You need to specify a song number to remove")
            return
        try:
            index = int(args[0])
        except ValueError:
            await send_message(ctx.channel, "You need to specify a valid song number to remove")
            return
        if index < 1 or index > len(self.queue):
            await send_message(ctx.channel, "You need to specify a valid song number to remove")
            return
        song = self.queue.pop(index - 1)
        await send_message(ctx.channel, f"Removed song #{index}: {song.title} :speak_no_evil:")

    @commands.command(name="move", aliases=["mv"], help="Moves a song in the queue")
    async def move(self, ctx, *args):
        logger.info("Move called")
        if len(args) < 2:
            await send_message(ctx.channel, "You need to specify a song number to move and a new position like ```!move 1 3```")
            return
        try:
            index = int(args[0])
            new_index = int(args[1])
        except ValueError:
            await send_message(ctx.channel, "You need to specify valid song numbers to move")
            return
        if index < 1 or index > len(self.queue) or new_index < 1 or new_index > len(self.queue):
            await send_message(ctx.channel, "You need to specify valid song numbers to move")
            return
        song = self.queue.pop(index - 1)
        self.queue.insert(new_index - 1, song)
        await send_message(ctx.channel, f"Moved song #{index} to position #{new_index} :blush:")

    @commands.command(name="shuffle", aliases=["sh"], help="Shuffles the queue")
    async def shuffle(self, ctx):
        logger.info("Shuffle called")
        random.shuffle(self.queue)
        await send_message(ctx.channel, "Queue shuffled! :game_die:")
