import discord
import requests
from pytube import YouTube

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

# Define the voice client
voice = None

# Reads token from binary file
with open("config/token.bin", "rb") as binary_file:
    token = binary_file.read().decode()

# Function to get weather from OpenWeatherMap API
def get_weather(city):
    # Get API key from binary file
    with open("config/open_weather.bin", "rb") as binary_file:
        api_key = binary_file.read().decode()

    # Get weather from API
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    
    # Check if city was found
    if response.status_code == 404:
        return "I couldn't find that city! :sob:"

    # Convert response to JSON
    weather_data = response.json()

    # Get weather description
    weather_desc = weather_data['weather'][0]['description']

    # Get temperature in Celsius
    temp = weather_data['main']['temp']
    temp_celsius = round(temp - 273.15)

    # Get wind speed in km/h
    wind = weather_data['wind']['speed']
    wind_kmh = round(wind * 3.6)

    # Format weather message
    weather = f'{city.title()} Weather: {weather_desc}, {temp_celsius}°C, {wind_kmh} km/h'

    print(weather)

    return weather

# Prints a message to the console when the bot is ready
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# Responds to messages with "Hello, World!" when mentioned
@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return
    
    # Check if the bot is mentioned in the message
    if client.user in message.mentions:
        await message.channel.send("Hi! I'm a bot! I can only tell the weather for now. Try typing 'weather <city>'! :sunny:\n\nI'm still in development, so I'll be getting more features soon! :smile:")
    else:
        # Print message to console
        print("Message received: " + message.content)
        
        # If message has weather command, respond with weather
        # Example: weather london
        if message.content.startswith('weather'):
            message_contents = message.content.split(' ')

            if len(message_contents) < 2:
                response = "I don't know what city you want the weather for!"

            else:
                # Get the city name from the message
                city = message_contents[1]
                # Get the weather from the API
                weather = get_weather(city)
                # Send the weather to the Discord channel
                response = weather
            
            await message.channel.send(response)

        # If message has play command, play the song
        # Example: play https://www.youtube.com/watch?v=dQw4w9WgXcQ
        if message.content.startswith('play '):
            # Get the URL from the message
            url = message.content[5:]

            # Check if the user is in a voice channel
            if not message.author.voice:
                await message.channel.send("You need to be in a voice channel to use this command!")
                return

            # Create and play the MusicPlayer
            async with message.channel.typing():
                try:
                    yt = YouTube(url)
                    video_url = yt.streams.filter(only_audio=True).first().url
                    player = MusicPlayer(video_url)
                    await player.play(message)
                except Exception as e:
                    await message.channel.send(f"An error occurred: {str(e)}")
                    return

        # If message has stop command, stop the song
        # Example: stop
        elif message.content.startswith('stop'):
            try:
                await player.stop()
            except Exception as e:
                await message.channel.send(f"An error occurred: {str(e)}")

# Define the audio player
class MusicPlayer:
    def __init__(self, url):
        self.url = url
        self.is_playing = False
        self.voice = None
        self.player = None
        self.title = None

    async def play(self, ctx):
        if not self.is_playing:
            self.is_playing = True
            self.voice = await ctx.author.voice.channel.connect()
            self.player = self.voice.play(discord.FFmpegPCMAudio(self.url), after=self.on_music_end)
            await self.show_now_playing(ctx)

    async def on_music_end(self, error=None):
        self.is_playing = False
        if error:
            print(f'Player error: {error}')
        await self.voice.disconnect()

    async def show_now_playing(self, ctx):
        yt = YouTube(self.url)
        self.title = yt.title
        await ctx.send(f'Now playing: {self.title}')

    async def stop(self):
        if self.is_playing:
            self.player.stop()
            await self.voice.disconnect()
            self.is_playing = False

if __name__ == "__main__":
    # Run the bot
    client.run(token)
