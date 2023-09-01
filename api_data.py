from dotenv import load_dotenv
import requests
#from google.cloud import storage
import os
load_dotenv()

class CryptoCapMarket:
  def __init__(self, key):
    self.key = key

  def get_crypto_info_by_ids(self, ids, limit=10):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'X-CMC_PRO_API_KEY': self.key  # Add your API key to the request header
        }
    
    parameters = {
        'start':1,
        'limit': limit,
        'convert':'BRL',
        'id':','.join(ids)
    }

    response = requests.get(url, headers=headers, params=parameters)
    return response.json()


crypto = CryptoCapMarket(os.getenv('API_KEY'))
crypto_ids = ['1', '1027', '825']
limit = 5
crypto_data = crypto.get_crypto_info_by_ids(limit=limit, ids=crypto_ids)  # Call the method to get the data

print(crypto_data)