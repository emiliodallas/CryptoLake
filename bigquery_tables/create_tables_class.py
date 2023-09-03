from google.cloud import bigquery

def create_table(table_id, schema, project_id, dataset_id):
    client = bigquery.Client(project=project_id)
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    table = bigquery.Table(table_ref, schema=schema)
    client.create_table(table)
    print(f"Table '{table_id}' created")