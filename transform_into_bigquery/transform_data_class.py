from authenticate_cloud_storage import authenticate_cloud_storage
from authenticate_bigquery import authenticate_bigquery
from date_time import get_current_time
from csv_format import create_csv
from google.cloud import storage
import pandas as pd
import json
import os

class TransformCrypto():
    def __init__(self, project_id, bucket_id, dataset_id):
        self.project_id = project_id
        self.bucket_name = bucket_id
        self.current_datetime = get_current_time()
        self.dataset_id = dataset_id    

    def transform_bronze_to_silver(self, event, context):
        '''Retrieve data from Cloud Storage'''
        file_path = event['name']
        
        json_data, _ = authenticate_cloud_storage(project_id=self.project_id,
                                                bucket_name=self.bucket_name,
                                                file_path=file_path)
        
        stage, coin_name, _ = file_path.split('/', 2)

        if stage == 'bronze':

            data = json.loads(json_data)

            if coin_name == 'Bitcoin':
                
                data_dict = create_csv(data=data, id='1')

            elif coin_name == 'Ethereum':

                data_dict = create_csv(data=data, id='1027')

            elif coin_name == 'Tether':

                data_dict = create_csv(data=data, id='825')

            df = pd.DataFrame(data_dict)
            output_file_name = f'/tmp/data_{self.current_datetime}.csv'
            df.to_csv(output_file_name, index=False, mode='a')

            self.store_data_in_cloud_storage(coin_name=coin_name, 
                                             data_stage='silver', 
                                             file_path=output_file_name)        
        else:

            self.upload_data_in_bigquery(coin_name, file_path)
            pass

    def upload_data_in_bigquery(self, table_id, data_file):
        
        client, table_ref, bigquery_job_config = authenticate_bigquery(project_id=self.project_id,
                                                                        dataset_id=self.dataset_id,
                                                                        table_id=table_id)

        file_data, _ = authenticate_cloud_storage(project_id=self.project_id,
                                                bucket_name=self.bucket_name,
                                                file_path=data_file)

        temp_file_name = "/tmp/temp_data.csv"
        
        with open(temp_file_name, "w") as temp_file:
            temp_file.write(file_data)         

        with open(temp_file_name, "rb") as source_file:
            job = client.load_table_from_file(source_file, table_ref, 
                                              job_config=bigquery_job_config)

            job.result() 

        os.remove(temp_file_name)

    def store_data_in_cloud_storage(self, coin_name, data_stage, file_path):
        '''Store data in Cloud Storage'''
        client = storage.Client(project=self.project_id)
        bucket = client.get_bucket(self.bucket_name)

        folder = f'{data_stage}/{coin_name}'
        blob_name = f'{folder}/data_{self.current_datetime}.csv'
        
        blob = bucket.blob(blob_name)
        with open(file_path, 'rb') as file:
            blob.upload_from_file(file, content_type='text/csv')

        # Remove the temporary CSV file
        os.remove(file_path)