import requests
from utility.tokens import WIT_AI_TOKEN
from utility.logger import logger

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
    try:
        response = requests.get(WIT_API_ENDPOINT, headers=headers, params=params, timeout=5)
    except requests.exceptions.Timeout:
        logger.error(f"Wit.ai request timed out")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Wit.ai request error: {e}")
        return None
    
    data = response.json()
    return data

def get_intent(data, confidence_threshold=0.5):
    '''
    Returns the intent from the Wit.ai response

    Parameters:
        data (dict): The Wit.ai response

    Returns:
        intent (str): The intent
    '''
    intent = data['intents'][0]['name'] if data['intents'] else None

    # Check if the confidence is above the threshold
    if intent:
        confidence = data['intents'][0]['confidence']
        if confidence < confidence_threshold:
            logger.warning(f"Intent confidence below threshold: {confidence}")
            intent = None

    return intent

def get_sentiment(data, confidence_threshold=0.5):
    '''
    Returns the sentiment from the Wit.ai response

    Parameters:
        data (dict): The Wit.ai response

    Returns:
        sentiment (str): The sentiment
    '''
    traits = data['traits']
    sentiment = traits['wit$sentiment:sentiment'][0]['value'] if 'wit$sentiment:sentiment' in traits else None
    
    # Check if the confidence is above the threshold
    if sentiment:
        confidence = traits['wit$sentiment:sentiment'][0]['confidence']
        if confidence < confidence_threshold:
            logger.warning(f"Sentiment confidence below threshold: {confidence}")
            sentiment = None

    return sentiment

def get_location(data, confidence_threshold=0.5):
    '''
    Returns the location from the Wit.ai response

    Parameters:
        data (dict): The Wit.ai response

    Returns:
        location (str): The location
    '''
    entities = data['entities']
    location = entities['wit$location:location'][0]['resolved']['values'][0]['name'] if 'wit$location:location' in entities else None
    
    # Check if the confidence is above the threshold
    if location:
        confidence = entities['wit$location:location'][0]['confidence']
        if confidence < confidence_threshold:
            logger.warning(f"Location confidence below threshold: {confidence}")
            location = None
    
    return location

def get_bot_id(data):
    '''
    Returns the bot id from the Wit.ai response

    Parameters:
        data (dict): The Wit.ai response

    Returns:
        bot_id (str): The bot id
    '''
    entities = data['entities']
    bot_id = entities['wit$bot_id:bot_id'][0]['body'] if 'wit$bot_id:bot_id' in entities else None
    return bot_id

class WitNlp:
    def __init__(self, message):
        self.message = message
        self.data = wit_ai_request(message) if message else None
        self.intent = get_intent(self.data) if self.data else None
        self.location = get_location(self.data) if self.data else None
        self.bot_id = get_bot_id(self.data) if self.data else None

    def __repr__(self):
        return f"WitNlp(message='{self.message}', intent='{self.intent}', location='{self.location}')"

    def __str__(self):
        return f"Intent: {self.intent}, Location: {self.location}"