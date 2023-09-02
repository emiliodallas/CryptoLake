from google.cloud import bigquery

schema = [
    bigquery.SchemaField("Circulating_Supply", "FLOAT"),
    bigquery.SchemaField("Price", "FLOAT"),
    bigquery.SchemaField("Volume_Change_24h", "FLOAT"),
    bigquery.SchemaField("Percent_Change_1h", "FLOAT"),
    bigquery.SchemaField("Market_Cap", "FLOAT"),
    bigquery.SchemaField("Fully_Diluted_Market_Cap", "FLOAT"),
]

table_ids = ["Bitcoin", "Ethereum", "Tether"]

class CryptoMarketTables():
    def __init__(self, project_id, dataset_id):
        self.project_id = project_id
        self.dataset_id = dataset_id

    def create_table(self, table_id, schema):
        client = bigquery.Client(project=self.project_id)
        dataset_ref = client.dataset(self.dataset_id)
        table_ref = dataset_ref.table(table_id)
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
        print(f"Table '{table_id}' created")

def create_tables():
    cm_tables = CryptoMarketTables(project_id="cadastrachallenge", dataset_id="marketcrypto_data")

    for table_id in table_ids:
        cm_tables.create_table(table_id=table_id, schema=schema)

create_tables()
