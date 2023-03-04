import requests
import json
from utility.tokens import WIT_AI_TOKEN

# Define the Wit.ai API endpoint
WIT_API_ENDPOINT = 'https://api.wit.ai/message'

# Define a function to make a request to the Wit.ai API
def wit_ai_request(message):
    '''
    Returns the Wit.ai response

    Parameters:
        message (str): The message to send to the Wit.ai API

    Returns:
        data (dict): The Wit.ai response    
    '''
    # Define the Wit.ai API headers and parameters
    headers = {'Authorization': f'Bearer {WIT_AI_TOKEN}'}
    params = {'q': message}

    # Call the Wit.ai API to get the NLP response
    response = requests.get(WIT_API_ENDPOINT, headers=headers, params=params, timeout=5)
    data = response.json()
    return data

def get_intent(data):
    '''
    Returns the intent from the Wit.ai response

    Parameters:
        data (dict): The Wit.ai response

    Returns:
        intent (str): The intent
    '''
    intent = data['intents'][0]['name'] if data['intents'] else None
    return intent

def get_location(data):
    '''
    Returns the location from the Wit.ai response

    Parameters:
        data (dict): The Wit.ai response

    Returns:
        location (str): The location
    '''
    entities = data['entities']
    location = entities['wit$location:location'][0]['resolved']['values'][0]['name'] if 'wit$location:location' in entities else None
    return location
