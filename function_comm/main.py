import requests

def call_function(function_url, http_method="GET", payload=None):
    try:
        if http_method == "GET":
            response = requests.get(function_url)
        elif http_method == "POST":
            response = requests.post(function_url, json=payload)
        else:
            return None, "Invalid HTTP method"

        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"Function call failed with status code {response.status_code}"

    except Exception as e:
        return None, str(e)