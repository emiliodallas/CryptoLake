from google.cloud import storage
from datetime import datetime
import requests
import json
import os

class CryptomarketPipeline():
    def __init__(self, project_id):
        self.key = os.getenv('criptomarket_api_key')
        self.project_id = project_id
           
    def create_api_request_params(self, id):  
        """

        """
        headers = {
            'X-CMC_PRO_API_KEY': self.key
        }

        parameters = {
            'convert': 'USD',
            'id': id
        }
        print('Success running create_api_request_params')

        return headers, parameters

    def get_current_time(self):
        current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        return current_datetime
    
    print('Success running get_current_time')

    def get_crypto_info_by_ids(self, id):
        url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
        headers, parameters = self.create_api_request_params(id)

        response = requests.get(url, headers=headers, params=parameters)
        print('Success running get_crypto_info_by_ids')

        return response.json()

    def extract_api_load_storage(self):
        crypto_ids = [1, 1027, 825]
        coin_names = ['Bitcoin', 'Ethereum', 'Tether']


        [  
        self.store_data_in_cloud_storage(
            data=self.get_crypto_info_by_ids(id),
            coin_name=coin_name,
            data_stage='bronze'
        )
        for id, coin_name in zip(crypto_ids, coin_names)
        ]
        
        print('Success running extract_api_load_storage')


    def store_data_in_cloud_storage(self, data, coin_name, data_stage):
        '''Store data in Cloud Storage'''
        current_datetime = self.get_current_time()
        client = storage.Client(project=self.project_id)
        bucket = client.bucket('crypto-cap-market')
        folder = f'{data_stage}/{coin_name}'
        data_json = json.dumps(data)
        blob = bucket.blob(f'{folder}/data_{current_datetime}.json')
        blob.upload_from_string(data_json)

        print('Success running store_data_in_cloud_storage')

def caller(context):
    pipeline = CryptomarketPipeline(project_id='cadastrachallenge')
    pipeline.extract_api_load_storage()

    success = {"Data Added and Extracted"}
    return success
    