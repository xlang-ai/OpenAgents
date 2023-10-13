"""The Zapier plugin personnel openapi.yaml handling, since it is special case, we need to handle it separately"""
import os
import requests

FILE_PATH = os.path.dirname(os.path.abspath(__file__))


# You need to manage your actions first in https://nla.zapier.com/providers/

# Reload the openapi
def reload_openapi(api_key, openapi_json):
    # Original data
    headers = {"X-API-Key": api_key, }
    # Call read the openapi
    url = "https://nla.zapier.com/api/v1/exposed/"

    data = None
    while True:
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            break
        except Exception as e:
            print(e)
            # if an error occurs, continue to retry
            import time
            time.sleep(5)
            continue

    try:
        data = data['results']
    except Exception as e:
        print(e)
        return openapi_json, {}

    new_paths = {}
    for item in data:
        new_paths['/api/v1/exposed/{}/execute/'.format(item["id"])] = {
            'post': {  # assuming POST method for all operations
                'operationId': item['operation_id'],
                'description': item['description'],
                'parameters': [
                    {'name': k, 'in': 'query', 'required': True, 'schema': {'type': v}}
                    for k, v in item['params'].items()
                ],
                "security": {
                    "SessionAuth": [],
                    "AccessPointApiKeyHeader": [],
                    "AccessPointApiKeyQuery": [],
                    "AccessPointOAuth": []
                }
            }
        }

    openapi_json['paths'] = openapi_json['paths'] | new_paths

    return openapi_json, new_paths


# Reload the endpoints
def reload_endpoints(new_paths):
    new_endpoint2caller = {}
    for new_path in new_paths:
        # create the call function
        def call_api(input_json, api_key):
            import requests
            headers = {"X-API-Key": api_key}
            url = "https://nla.zapier.com" + new_path
            response = requests.post(url, headers=headers, json=input_json)

            if response.status_code == 200:
                return response.json()
            else:
                return response.text

        new_endpoint2caller[new_path] = call_api

    return new_endpoint2caller
