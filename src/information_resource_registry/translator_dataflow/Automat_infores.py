import requests
import re
import json

def fetch_automat_apis():
    all_apis = []

    # Translator API endpoint
    url = "https://smart-api.info/api/query"

    params = {
        "q": "Automat",
        "size": 10,  # 10 APIs returned per page
        "from": 0  # Multiple pages of Automat APIs
    }

    while True:
        # Find Automat APIs
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            all_apis.extend(data['hits'])
            total = data['total']
            current_from = params['from']

            # If we have fetched all the APIs, break
            if current_from + params['size'] >= total:
                break

            # Go to next page
            params['from'] += params['size']

        else:
            print(f"Failed to retrieve data. Status code: {response.raise_for_status()}")

    return all_apis


def extract_names(apis):

    # Regex pattern to get name
    # Automat- : Start at the string "Automat-".
    # ([ ^ ()]+) : match everything that is not a parenthesis until it encounters "(".
    # \( : stop at the string  "(".
    pattern = r'Automat-([^()]+)\('

    extracted_items = []
    for item in apis:
        match = re.search(pattern, item)
        if match:
            extracted_items.append(match.group(1))

    return extracted_items


def fetch_metadata(apis_infores):

    infores_dict = {}

    for source, infores in apis_infores.items():
        print(source)

        # These sources have different names on SmartAPI vs Automat
        if source =='robokop':
            source = 'robokopkg'
        if source == 'monarchinitiative':
            source = 'monarch-kg'
        if source == 'drug-central':
            source = 'drugcentral'
        if source == 'hetionet':
            source = 'hetio'

        if source == 'robokopkg':
            url = f"https://automat.renci.org/{source}/metadata"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                infores_dict[infores] = data["qc_results"]["primary_knowledge_sources"]
            else:
                print(f"Failed to retrieve metadata for source: {source}. Status code: {response.status_code}")
                infores_dict[infores] = ['Failed API call']

        elif source in ['monarch-kg', 'icees-kg']:
            url = f"https://automat.renci.org/{source}/metadata"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                infores_dict[infores] = [data["provenanceTag"]]
            else:
                print(f"Failed to retrieve metadata for source: {source}. Status code: {response.status_code}")
                infores_dict[infores] = ['Failed API call']

        else:
            url = f"https://automat.renci.org/{source}/metadata"
            response = requests.get(url)

            # This works for all Automat sources except robokopkg, monarch-kg, and icees-kg
            if response.status_code == 200:
                data = response.json()
                qc = data["qc_results"]
                primary_ks = qc["primary_knowledge_sources"]
                provenance = data["sources"][0]["provenance"]
                infores_dict[infores] = primary_ks

            else:
                print(f"Failed to retrieve metadata for source: {source}. Status code: {response.status_code}")
                infores_dict[infores] = ['Failed API call']

    return infores_dict

def main():
    '''
    This a bit wonky and I suggest improvements, but this is how it runs now:
    1) Get all the sources from smart api that start with "Automat"
    2) Get the title of those sources: ie Automat-robokop(Trapi v1.5.0)
    3) Extract just the knowledge provider name: ie robokop
    4) Get the metadata of those sources from the automat endpoint: https://automat.renci.org/#/robokopkg
        4a) If the knowledge provided name is not the same as the automat name, fix it
    5) Make a dictionary  provenance: primary_knowledge_source

    There should be a way to get the meta data directly from the smartAPI endpoint, but that requires getting
    the smartAPI ID. There was no obvious way to do this (to me).
    If the smartAPI ID can be obtained, then steps 2-4 are not necessary.
    '''

    all_apis = fetch_automat_apis()

    automat_apis = {api['info']['title']: api['info']['x-translator']['infores'] for api in all_apis}

    KPs = extract_names(automat_apis.keys())

    automat_api_infores = {kp: automat_apis[title] for kp, title in zip(KPs, automat_apis.keys())}
    infores_dict = fetch_metadata(automat_api_infores)

    for k, v in infores_dict.items():
        # Sort the list in alphabetical order
        infores_dict[k].sort()

    with open('src/information_resource_registry/translator_dataflow/data/automat_infores_list.json', 'w') as outfile:
        json.dump(infores_dict, outfile, indent=2, sort_keys=True)

    print("File successfully saved in alphabetical order.")

if __name__ == "__main__":
    main()
