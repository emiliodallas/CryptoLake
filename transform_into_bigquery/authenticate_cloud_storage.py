from google.cloud import storage

def authenticate_cloud_storage(project_id, bucket_name, file_path):
    client = storage.Client(project=project_id)
    bucket = client.get_bucket(bucket_name)  

    blob = bucket.blob(file_path)
    file_data = blob.download_as_text()

    return file_data, blob