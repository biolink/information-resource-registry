import requests
import yaml
import json

def main():
    infores_dict = {'infores:rtx-kg2': []}

    url = "https://raw.githubusercontent.com/RTXteam/RTX-KG2/master/maps/kg2-provided-by-curie-to-infores-curie.yaml"
    response = requests.get(url)

    if response.status_code == 200:
        knowledge_sources = yaml.safe_load(response.content)

        for curie, infores_curie in knowledge_sources.items():
            if infores_curie['infores_curie'] != 'infores:rtx-kg2':
                infores_dict['infores:rtx-kg2'].append(infores_curie['infores_curie'])
    else:
        print(f"Error downloading file: {response.status_code}")
        exit()

    json.dump(infores_dict, open('src/information_resource_registry/relation_map/data/rtx-kg2.json', 'w'), indent=2, sort_keys=True)

# Call main() if this script is executed directly
if __name__ == "__main__":
    main()