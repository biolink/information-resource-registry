import requests
import json


url = 'https://translator.broadinstitute.org/molecular_data_provider/transformers'
response = requests.get(url)

if response.status_code == 200:
    resources = set()
    for transformer in response.json():
        name = transformer['name']
        infores = transformer['infores']
        resources.add(infores)
    resources = list(resources)
    resources.sort()
    infores_dict = {'infores:molepro': resources}
    json.dump(infores_dict, open('data/molepro_resources.json', 'w'), indent=2, sort_keys=True)
    print('Fetched and saved', len(resources), 'resources')
else:
    print('Failed to fetch data:', response.status_code)