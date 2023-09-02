from google.cloud import storage, secretmanager
from datetime import datetime
from flask import jsonify
import pandas as pd
import requests
import json

class CryptomarketPipeline:
    def __init__(self, key):
        self.key = key
    
    def get_secret(self, project_id, secret_id):
        """

        """
        try:
            client = secretmanager.SecretManagerServiceClient()
            name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
            response = client.access_secret_version(name=name)
            secret_value = response.payload.data.decode("UTF-8")
            secret_string = json.loads(secret_value)
            self.key = secret_value   
            return secret_string  
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    def create_api_request_params(self, id):  
        """

        """
        api_key = self.get_secret(project_id="cadastrachallenge", secret_id="cryptomarket_api_key")  
        headers = {
            'X-CMC_PRO_API_KEY': api_key
        }

        parameters = {
            'convert': 'USD',
            'id': id
        }
        return headers, parameters

    def get_current_time(self,):
        current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        return current_datetime

    def get_crypto_info_by_ids(self, id):
        url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
        headers, parameters = self.create_api_request_params(id)

        response = requests.get(url, headers=headers, params=parameters)
        return response.json()

    def run_functions(self):
        crypto_ids = ['1', '1027', '825']
        coin_names = ['Bitcoin', 'Ethereum', 'Tether']

        for id, coin_name in zip(crypto_ids, coin_names):
            response = self.get_crypto_info_by_ids(id)
            self.store_data_in_cloud_storage(response, coin_name, data_stage='bronze')


    def store_data_in_cloud_storage(self, data, coin_name, data_stage):
        '''Store data in Cloud Storage'''
        current_datetime = self.get_current_time()
        client = storage.Client()
        bucket = client.bucket('cripto-cap-market')
        folder = f'{data_stage}/{coin_name}'
        blob = bucket.blob(f'{folder}/data_{current_datetime}.json')  # Include date and time in the filename
        blob.upload_from_string(data)
