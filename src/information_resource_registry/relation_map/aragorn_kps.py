import requests
import json

infores_dict = {"infores:aragorn": []}


def main():
    url = "https://strider.ci.transltr.io/kps"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            kps = response.json()

            infores_dict["infores:aragorn"] = kps

            with open('src/information_resource_registry/relation_map/data/aragorn_to_kps.json', 'w') as outfile:
                json.dump(infores_dict, outfile, indent=2, sort_keys=True)
        except Exception as e:
            print(f"Failed to parse list of KPs from Aragorn: {e}")
    else:
        print(f"Failed to download list of KPs from Aragorn with status code: {response.status_code}.")

if __name__ == "__main__":
    main()
