from create_tables_class import create_table
from google.cloud import bigquery

def create_tables():
    for table_id in table_ids:
        create_table()(table_id=table_id, schema=schema, 
                       project_id="cadastrachallenge", 
                       dataset_id="marketcrypto_data")
        
schema = [
    bigquery.SchemaField("Circulating_Supply", "FLOAT"),
    bigquery.SchemaField("Price", "FLOAT"),
    bigquery.SchemaField("Volume_Change_24h", "FLOAT"),
    bigquery.SchemaField("Percent_Change_1h", "FLOAT"),
    bigquery.SchemaField("Market_Cap", "FLOAT"),
    bigquery.SchemaField("Fully_Diluted_Market_Cap", "FLOAT"),
]

table_ids = ["Bitcoin", "Ethereum", "Tether"]
        
create_tables()