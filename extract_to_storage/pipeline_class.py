from date_time import get_current_time
from authenticate_cloud_storage import authenticate_cloud_storage
import requests
import json
import os

class CryptomarketPipeline():
    def __init__(self, project_id, key_id, bucket_id):
        self.key = os.getenv(key_id)
        self.project_id = project_id
        self.bucket_name = bucket_id
           
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
        return headers, parameters

    def get_crypto_info_by_ids(self, id):
        url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
        headers, parameters = self.create_api_request_params(id)

        response = requests.get(url, headers=headers, params=parameters)

        return response.json()

    def store_data_in_cloud_storage(self, data, coin_name, data_stage):
        client, bucket =  authenticate_cloud_storage(self.project_id,
                                                     self.bucket_name)

        folder = f'{data_stage}/{coin_name}'
        current_datetime = get_current_time()

        data_json = json.dumps(data)

        blob = bucket.blob(f'{folder}/data_{current_datetime}.json')
        blob.upload_from_string(data_json)

    def extract_api_data(self):
        [  
        self.store_data_in_cloud_storage(
            data=self.get_crypto_info_by_ids(id),
            coin_name=coin_name,
            data_stage='bronze'
        )
        for id, coin_name in zip(crypto_ids, coin_names)
        ]
        success = {"Data Added and Extracted"}
        return success

crypto_ids = [1, 1027, 825]
coin_names = ['Bitcoin', 'Ethereum', 'Tether']