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
* !join - Joins the voice channel you are in
* !help - Displays a list of commands
* !play <youtube url> - Plays / adds a song to the queue
* !add <youtube url> - Plays / adds a song to the queue
* !pause - Pauses / Resumes the current song
* !resume - Resumes the current song
* !skip - Skips the current song
* !queue <depth> - Displays the queue (depth argument optional)
* !clear - Clears the current queue
* !stop - Stops the current song, clears the queue and leaves the voice channel
* !remove <index> - Removes the specified song from the queue
* !move <index> <new index> - Moves the specified song to the new index position
* !shuffle - Shuffles the queue