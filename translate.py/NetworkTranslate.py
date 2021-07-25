import requests, uuid, json

subscription_key = ""
endpoint = ""
location = ""

path = '/translate'
constructed_url = endpoint + path

params = {
    'api-version': '3.0',
    'from': 'es',
    'to': ['en', 'fr', 'es']
}
constructed_url = endpoint + path

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

body = [{
    'text': 'es que python es lo mejor'
}]

request = requests.post(constructed_url, params=params, headers=headers, json=body)
response = request.json()

print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
