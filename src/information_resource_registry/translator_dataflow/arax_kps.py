import requests
import json

def main():
    infores_dict = {'infores:arax': []}

    url = "https://arax.ci.transltr.io/api/arax/v1.4/status?authorization=smartapi"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            smartapi_entries = response.json()

            for entry in smartapi_entries:
                if entry.get('component') == 'KP':
                    infores_dict['infores:arax'].append(entry.get('infores_name', 'Unknown'))

            # Sort the list in alphabetical order
            infores_dict['infores:arax'].sort()

            with open('src/information_resource_registry/translator_dataflow/data/arax_infores_list.json', 'w') as outfile:
                json.dump(infores_dict, outfile, indent=2, sort_keys=True)

            print("File successfully saved in alphabetical order.")
        except json.JSONDecodeError:
            print("Error decoding the JSON response.")
    else:
        print(f"Error downloading file: {response.status_code}")

if __name__ == "__main__":
    main()
