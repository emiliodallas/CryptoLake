from google.cloud import secretmanager
from flask import jsonify

def get_secret(request):
    try:
        # Access the secret
        project_id = "cadastrachallenge"
        secret_id = "cryptomarket_api_key"
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(name=name)
        secret_value = response.payload.data.decode("UTF-8")
        
        # Return the secret value as a JSON response
        return jsonify({'secret_value': secret_value}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500