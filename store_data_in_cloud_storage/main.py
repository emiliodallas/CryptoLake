from google.cloud import storage
from datetime import datetime

def store_data_in_cloud_storage(data, coin_name, data_stage):
    '''Store data in Cloud Storage'''
    current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    client = storage.Client()
    bucket = client.bucket('cripto-cap-market')
    folder = f'{data_stage}/{coin_name}'
    blob = bucket.blob(f'{folder}/data_{current_datetime}.json')  # Include date and time in the filename
    blob.upload_from_string(data)