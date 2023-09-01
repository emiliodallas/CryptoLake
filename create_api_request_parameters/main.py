import requests

def create_api_request_params(id):
    function_url = 'https://us-central1-cadastrachallenge.cloudfunctions.net/get_secret'
    
    try:
        response = requests.get(function_url)
        if response.status_code == 200:
            api_key = response.json().get('cryptomarket_api_key')  # Replace 'api_key' with the actual key name in the JSON response
            headers = {
                'X-CMC_PRO_API_KEY': api_key
            }
            print(api_key)
            return headers
        else:
            return None, f"Function call failed with status code {response.status_code}"
    except Exception as e:
        return None, str(e)