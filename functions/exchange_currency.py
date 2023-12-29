import requests
#from utility.tokens import EXCHANGE_RATE_TOKEN
#from utility.logger import logger

EXCHANGE_RATE_TOKEN = '26txEcOhY4nJeB3E2ELMlgy6MRceiU6c'
'''
url = "https://api.apilayer.com/exchangerates_data/convert?to=GBP&from=ZAR&amount=10"

payload = {}
headers= {
  "apikey": EXCHANGE_RATE_TOKEN
}

response = requests.request("GET", url, headers=headers, data=payload)

status_code = response.status_code
result = response.text
json = response.json()

print(result)
'''
def exchange_rate_request(from_currency, to_currency, amount):
    '''
    Returns the exchange rate from one currency to another

    Parameters:
        from_currency (str): The currency to convert from
        to_currency (str): The currency to convert to
        amount (float): The amount to convert

    Returns:
        exchange_rate (float): The exchange rate
    '''
    # Define the Exchange Rate API endpoint
    EXCHANGE_RATE_API_ENDPOINT = 'https://api.apilayer.com/exchangerates_data/convert'

    # Define the Exchange Rate API headers and parameters
    headers = {'apikey': EXCHANGE_RATE_TOKEN}
    params = {
        'from': from_currency, 
        'to': to_currency, 
        'amount': amount
        }

    # Call the Exchange Rate API to get the exchange rate
    try:
        response = requests.get(EXCHANGE_RATE_API_ENDPOINT, headers=headers, params=params, timeout=5)
    except requests.exceptions.Timeout:
        #logger.error(f"Exchange Rate request timed out")
        print('Exchange Rate request timed out')
        return None
    except requests.exceptions.RequestException as e:
        #logger.error(f"Exchange Rate request error: {e}")
        print(e)
        return None
    
    data = response.json()
    exchange_rate = data['result']
    return exchange_rate

print(exchange_rate_request('ZAR', 'GBP', 100))