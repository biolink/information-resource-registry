
# imports
import requests
import json

# constants
KEY_STATIC_RESOURCES = "static_external"

# methods
def main():
    url = 'https://raw.githubusercontent.com/broadinstitute/genetics-kp-dev/refs/heads/master/python-flask-server/conf/informationResources.json'
    response = requests.get(url)

    if response.status_code == 200:
        try:
            json_response = response.json()
            # get the static resources
            map_static_resources = json_response.get(KEY_STATIC_RESOURCES)

        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")

        # Save the resources to a JSON file
        try:
            with open('src/information_resource_registry/translator_dataflow/data/geneticskp_resources.json', 'w') as outfile:
                json.dump(map_static_resources, outfile, indent=2, sort_keys=True)

            print('Saved infores: {}'.format(json.dumps(map_static_resources, indent=2)))

        except Exception as e:
            print(f"Failed to write JSON to file: {e}")
    else:
        print('Failed to fetch data:', response.status_code)


# main 
if __name__ == "__main__":
    main()
