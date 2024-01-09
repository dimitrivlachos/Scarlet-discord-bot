# Scarlet AI
 
A natural language processing bot that uses Wit.ai to understand what you are saying and respond accordingly.

## Setup
You will need to create another folder called 'config' and within it create a .bin files for several api tokens. 
* Discord api token
* Open weather api token
* Wit.ai api token

You can use the text_to_bin.py file in /utility to convert your tokens and api keys to .bin files. By typing in the command line:
```python text_to_bin.py "<api key>" token.bin```

## NLP Capabilities
* Responds to weather requests
* Responds to dice rolls

## Commands
* !help - Displays a list of commands
* !play <youtube url> - Plays a youtube video in the voice channel you are in
* !add <youtube url> - Adds a youtube video to the queue
* !pause - Pauses / Resumes the current song
* !resume - Resumes the current song
* !skip - Skips the current song
* !queue - Displays the current queue
* !clear - Clears the current queue
* !stop - Stops the current song and leaves the voice channel
* !remove - Removes the last song added to the queue