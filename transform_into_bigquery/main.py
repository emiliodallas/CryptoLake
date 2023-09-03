from transform_data_class import TransformCrypto

def transformer(event, context):
    trans_crypto = TransformCrypto(project_id='cadastrachallenge', 
                                   bucket_id='crypto-cap-market', 
                                   dataset_id='marketcrypto_data')
    
    trans_crypto.transform_bronze_to_silver(event, context)