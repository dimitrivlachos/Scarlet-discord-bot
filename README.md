# Scarlet AI
 
My very own discord bot!

## Setup
You will need to create another folder called 'config' and within it create a .bin files for several api tokens. 
* Discord api token
* Open weather api token
* Wit.ai api token

You can use the text_to_bin.py file in /utility to convert your tokens and api keys to .bin files. By typing in the command line:
```python text_to_bin.py "<api key>" token.bin```

## Commands
Scarlet AI does not have a prefix, instead, she uses Wit.ai to understand what you are saying through natural language processing.

So far, Scarlet AI can do the following:
* Get the weather for a town or city mentioned
* Roll dice using the format 'roll 2d6'
* Respond to someone saying that they're sick with a get well soon message
* ~~Get the current time in a city mentioned~~
* ~~Respond to a 'hello' or 'hi' with a greeting~~