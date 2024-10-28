import requests
import yaml
import json

def main():
    infores_dict = {'infores:unsecret-agent': []}

    url = "https://raw.githubusercontent.com/webyrd/mediKanren/refs/heads/master/medikanren2/neo/neo-open-api/unsecret-source-consume.yaml"
    response = requests.get(url)

    if response.status_code == 200:
        knowledge_sources = yaml.safe_load(response.content)

        for curie, infores_curie in knowledge_sources.items():
          infores_dict['infores:unsecret-agent'].append(infores_curie['infores_curie'])
    else:
        print(f"Error downloading file: {response.status_code}")
        exit()

    json.dump(infores_dict, open('data/unsecret.json', 'w'), indent=2, sort_keys=True)

# Call main() if this script is executed directly
if __name__ == "__main__":
    main()
