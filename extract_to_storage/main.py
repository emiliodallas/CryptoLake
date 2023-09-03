import pipeline_class

def caller(context):
    pipeline = pipeline_class.CryptomarketPipeline(project_id='cadastrachallenge', key_id='criptomarket_api_key', bucket_id='crypto-cap-market')
    pipeline.extract_api_data()   