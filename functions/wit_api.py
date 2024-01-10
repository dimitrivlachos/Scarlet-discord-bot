import aiohttp
import asyncio
from utility.tokens import WIT_AI_TOKEN
from utility.logger import logger

# Define the Wit.ai API endpoint
WIT_API_ENDPOINT = 'https://api.wit.ai/message'

# Define an asynchronous function to make a request to the Wit.ai API
async def wit_ai_request(message):
    '''
    Returns the Wit.ai response

    Parameters:
        message (str): The message to send to the Wit.ai API

    Returns:
        data (dict): The Wit.ai response    
    '''
    logger.info(f"Sending message to Wit.ai: {message}")
    
    # Define the Wit.ai API headers and parameters
    headers = {'Authorization': f'Bearer {WIT_AI_TOKEN}'}
    params = {'q': message}

    # Call the Wit.ai API to get the NLP response
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(WIT_API_ENDPOINT, headers=headers, params=params, timeout=5) as response:
                data = await response.json()
                return data
        except asyncio.TimeoutError:
            logger.error(f"Wit.ai request timed out")
            return None
        except aiohttp.ClientError as e:
            logger.error(f"Wit.ai request error: {e}")
            return None

class WitNlp:
    def __init__(self):
        self.message = ""
        self.intents = []
        self.entities = {}
        self.text = ""
        self.trait = {}

    async def load(self, message):
        self.message = message

        # Call the Wit.ai API to get the NLP response
        response = await wit_ai_request(message)
        if response:
            self.intents = [intent(
                name=i['name'], 
                confidence=i['confidence']
                ) for i in response.get('intents', [])] # Pull out each intent
            self.entities = response.get('entities', {})
            self.text = response.get('text', "")
            self.trait = response.get('traits', {})

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