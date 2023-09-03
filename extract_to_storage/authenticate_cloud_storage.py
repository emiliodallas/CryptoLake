from google.cloud import storage

def authenticate_cloud_storage(project_id, bucket_name):
    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)        

    return client, bucket