from authenticate_cloud_storage import authenticate_cloud_storage
from date_time import get_current_time
from error_handling import errors
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
        
        try:
            response = requests.get(url, headers=headers, params=parameters)
            response.raise_for_status()  
            errors(response.status_code)
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error while making API request: {e}")

            return None  

    def store_data_in_cloud_storage(self, data, coin_name, data_stage):
        client, bucket =  authenticate_cloud_storage(self.project_id,
                                                     self.bucket_name)

        folder = f'{data_stage}/{coin_name}'
        current_datetime = get_current_time()

        data_json = json.dumps(data)

        blob = bucket.blob(f'{folder}/data_{current_datetime}.json')
        blob.upload_from_string(data_json)

    def extract_api_data(self):
        try:
            [  
            self.store_data_in_cloud_storage(
                data=self.get_crypto_info_by_ids(id),
                coin_name=coin_name,
                data_stage='bronze'
            )
            for id, coin_name in zip(crypto_ids, coin_names)
            ]

        except:
            print("Check Raised Exception For Error")
            return None

crypto_ids = [1, 1027, 825]
coin_names = ['Bitcoin', 'Ethereum', 'Tether']