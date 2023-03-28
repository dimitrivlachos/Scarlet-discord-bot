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

class WitNlp:
    def __init__(self, message):
        self.message = message

        # Call the Wit.ai API to get the NLP response
        response = wit_ai_request(message)

        # Get the intent
        self.intents = [intent(
            name=i['name'], 
            confidence=i['confidence']
            ) for i in response['intents']] # Pull out each intent
        
        self.entities = response['entities']
        self.text = response['text']
        self.trait = response['traits']

    def __repr__(self):
        return f"WitNlp(message='{self.message}')"

    def __str__(self):
        return f"WitNlp(message='{self.message}')"
    
class intent:
    def __init__(self, name, confidence):
        self.name = name
        self.confidence = confidence
        self.confidence_percent = round(confidence, 2)

    def __repr__(self):
        return f"{self.name} ({self.confidence} confidence)"

    def __str__(self):
        return f"{self.name} ({self.confidence_percent}% confidence)"