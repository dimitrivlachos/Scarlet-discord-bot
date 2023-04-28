import requests
#from utility.tokens import EXCHANGE_RATE_TOKEN
#from utility.logger import logger

url = "https://api.apilayer.com/exchangerates_data/convert?to=GBP&from=USD&amount=10"

payload = {}
headers= {
  "apikey": "26txEcOhY4nJeB3E2ELMlgy6MRceiU6c"
}

response = requests.request("GET", url, headers=headers, data = payload)

status_code = response.status_code
result = response.text

print(result)