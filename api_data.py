from google.cloud import storage, secretmanager
from datetime import datetime
import pandas as pd
import requests
import json
from flask import jsonify, request

app = Flask(__name__)

def get_secret(request):
    try:
        # Access the secret
        project_id = "cadastrachallenge"
        secret_id = "cryptomarket_api_key"
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(name=name)
        secret_value = response.payload.data.decode("UTF-8")
        
        # Return the secret value as a JSON response
        return jsonify({'secret_value': secret_value}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_crypto_info_by_ids(id):
    crypto_ids = ['1', '1027', '825']
    coin_names = ['Bitcoin', 'Ethereum', 'Tether']
    function_url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
     
    try:
        response = requests.get(function_url)
        if response.status_code == 200:
            api_key = response.json().get('cryptomarket_api_key')  # Replace 'api_key' with the actual key name in the JSON response
            headers = {
                'X-CMC_PRO_API_KEY': api_key
            }
            print(api_key)
            return headers
        for crypto_id, coin_name in zip(crypto_ids, coin_names):
            url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
            payload = {
                'convert': 'USD',
                'id': id
            }
            try:
                response = requests.get(url, headers=headers, params=payload)
                if response.status_code == 200:
                    store_data_url = 'https://your-cloud-function-url/store_data'
                    payload = {
                        'data': response.json(),
                        'coin_name': coin_name,
                        'data_stage': 'bronze'
                    
                    }
                    try:
                        response = requests.post(store_data_url, json=payload)
                        if response.status_code != 200:
                            print(f"Function call failed with status code {response.status_code}")
                    except Exception as e:
                        print(str(e))
                else:
                    print(f"Function call failed with status code {response.status_code}")
            except Exception as e:
                print(str(e))
        else:
            return f"Function call failed with status code {response.status_code}"
    except Exception as e:
        return str(e)
    
@app.route('/store_data', methods=['POST'])
def store_data_in_cloud_storage(data, coin_name, data_stage):

    try:
        data = request.json.get('data')
        coin_name = request.json.get('coin_name')
        data_stage = request.json.get('data_stage')

        current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        client = storage.Client()
        bucket = client.bucket('cripto-cap-market')
        folder = f'{data_stage}/{coin_name}'
        blob = bucket.blob(f'{folder}/data_{current_datetime}.json')
        blob.upload_from_string(data)

        return jsonify({"message": "Data stored successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def transform_bronze_to_silver(event, context):
    '''Retrieve data from Cloud Storage'''
    file_name = event['name']
    bucket_name = event['cripto-cap-market']

    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)

    json_data = blob.download_as_text()
    data = json.loads(json_data)

    coin_data = data['data']['1']  # Assuming you're interested in the data for the coin with ID 1
    coin_name=coin_data['name']
    circulating_supply = coin_data['circulating_supply']
    price = coin_data['quote']['USD']['price']
    volume_change_24h = coin_data['quote']['USD']['volume_change_24h']
    percent_change_1h = coin_data['quote']['USD']['percent_change_1h']
    market_cap = coin_data['quote']['USD']['market_cap']
    fully_diluted_market_cap = coin_data['quote']['USD']['fully_diluted_market_cap']

    data_dict = {
    'Circulating Supply': [circulating_supply],
    'Price': [price],
    'Volume Change 24h': [volume_change_24h],
    'Percent Change 1h': [percent_change_1h],
    'Market Cap': [market_cap],
    'Fully Diluted Market Cap': [fully_diluted_market_cap]
    }

    df = pd.DataFrame(data_dict)

    current_datetime = get_current_time()
    output_file_name = f'data_{current_datetime}.csv'

    csv = df.to_csv(output_file_name, index=False)
    store_data_in_cloud_storage(csv, coin_name, data_stage='silver')