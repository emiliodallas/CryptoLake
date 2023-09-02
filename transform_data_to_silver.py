from google.cloud import storage, secretmanager
from datetime import datetime
import pandas as pd
import requests
import json

class TransformCrypto():
    def get_current_time(self,):
        current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        return current_datetime

    def transform_bronze_to_silver(self, event, context):
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

        current_datetime = self.get_current_time()
        output_file_name = f'data_{current_datetime}.csv'

        csv = df.to_csv(output_file_name, index=False)
        store_data_in_cloud_storage(csv, coin_name, data_stage='silver')

    def store_data_in_cloud_storage(self, data, coin_name, data_stage):
        '''Store data in Cloud Storage'''
        current_datetime = self.get_current_time()
        client = storage.Client()
        bucket = client.bucket('cripto-cap-market')
        folder = f'{data_stage}/{coin_name}'
        blob = bucket.blob(f'{folder}/data_{current_datetime}.json')  # Include date and time in the filename
        blob.upload_from_string(data)