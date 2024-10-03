import requests
import json


def main():
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

        # Save the resources to a JSON file
        with open('src/information_resource_registry/relation_map/data/molepro_resources.json', 'w') as file:
            json.dump(infores_dict, file, indent=2, sort_keys=True)

        print('Fetched and saved', len(resources), 'resources')
    else:
        print('Failed to fetch data:', response.status_code)


# Call main() if this script is executed directly
if __name__ == "__main__":
    main()