import requests

def get_crypto_info_by_ids(id):
  url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
  headers, parameters = create_api_request_params(id)

  response = requests.get(url, headers=headers, params=parameters)
  return response.json()