from google.cloud import storage, bigquery
from datetime import datetime
import pandas as pd
import json
import os

class TransformCrypto():
    def __init__(self, project_id):
        self.project_id = project_id
        self.bucket_name = 'crypto-cap-market'
        self.current_datetime = self.get_current_time()
        self.dataset_id = 'marketcrypto_data'

    def get_current_time(self,):
        current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        return current_datetime

    def create_csv(self, data, id):
        coin_data = data['data'][id]
        circulating_supply = coin_data['circulating_supply']
        price = coin_data['quote']['USD']['price']
        volume_change_24h = coin_data['quote']['USD']['volume_change_24h']
        percent_change_1h = coin_data['quote']['USD']['percent_change_1h']
        market_cap = coin_data['quote']['USD']['market_cap']
        fully_diluted_market_cap = coin_data['quote']['USD']['fully_diluted_market_cap']

        data_dict = {
        'Circulating_Supply': [circulating_supply],
        'Price': [price],
        'Volume_Change_24h': [volume_change_24h],
        'Percent_Change_1h': [percent_change_1h],
        'Market_Cap': [market_cap],
        'Fully_Diluted_Market_Cap': [fully_diluted_market_cap]
        }
        return data_dict

    def transform_bronze_to_silver(self, event, context):
        '''Retrieve data from Cloud Storage'''
        file_path = event['name']
        bucket_name = event['bucket']
        
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)

        stage, coin_name, _ = file_path.split('/', 2)
        if stage == 'bronze':
            
            print(file_path)

            blob = bucket.blob(file_path)

            json_data = blob.download_as_text()
            print(json_data)
            data = json.loads(json_data)

            if coin_name == 'Bitcoin':
                
                data_dict = self.create_csv(data=data, id='1')
                print(data_dict)

            elif coin_name == 'Ethereum':

                data_dict = self.create_csv(data=data, id='1027')
                print(data_dict)

            elif coin_name == 'Tether':

                data_dict = self.create_csv(data=data, id='825')
                print(data_dict)

            df = pd.DataFrame(data_dict)

            output_file_name = f'/tmp/data_{self.current_datetime}.csv'

            df.to_csv(output_file_name, index=False, mode='a')
            self.store_data_in_cloud_storage(coin_name=coin_name, data_stage='silver', file_path=output_file_name)
        else:
            print("data is silver? R: ", stage)
            print(file_path)
            self.upload_data_in_bigquery(coin_name, file_path)
            pass

    def upload_data_in_bigquery(self, table_id, data_file):
        client = bigquery.Client(project=self.project_id)
        dataset_ref = client.dataset(self.dataset_id)
        table_ref = dataset_ref.table(table_id)

        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.CSV
        job_config.skip_leading_rows = 1 

        with open(data_file, "rb") as source_file:
            job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

            job.result()  # Wait for the job to complete   
        print("##############JOB INSERTED INTO BIGQUERY##############")

    def store_data_in_cloud_storage(self, coin_name, data_stage, file_path):
        '''Store data in Cloud Storage'''
        client = storage.Client(project=self.project_id)
        bucket = client.get_bucket(self.bucket_name)

        folder = f'{data_stage}/{coin_name}'
        blob_name = f'{folder}/data_{self.current_datetime}.csv'
        
        # Upload the CSV file to Cloud Storage
        blob = bucket.blob(blob_name)
        with open(file_path, 'rb') as file:
            blob.upload_from_file(file, content_type='text/csv')

        # Remove the temporary CSV file
        os.remove(file_path)

def transformer(event, context):
    trans_crypto = TransformCrypto(project_id='cadastrachallenge')
    trans_crypto.transform_bronze_to_silver(event, context)