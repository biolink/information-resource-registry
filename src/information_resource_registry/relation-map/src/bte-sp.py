import requests
import json
import yaml

# Get x-bte smartapi specs
url = "https://smart-api.info/api/query?q=tags.name:translator&size=1000&sort=_seq_no&raw=1&fields=paths,servers,tags,components.x-bte*,info,_meta"
response = requests.get(url)

try:
    response.raise_for_status()
except Exception:
    print(f"error downloading smartapi specs: {response.status_code}")
    exit()

smartapi = json.loads(response.content)

# Get BTE API list
url = "https://raw.githubusercontent.com/biothings/bte-server/main/config/api_list.yaml"
response = requests.get(url)

try:
    response.raise_for_status()
except Exception:
    print(f"error downloading BTE API List: {response.status_code}")
    exit()

bte_list = yaml.safe_load(response.content)

# Build KP -> API infores mapping
sources_by_kps: dict[str, set] = {}
hits_by_infores = {}
for hit in smartapi["hits"]:
    if "infores" not in hit["info"]["x-translator"]:
        continue
    kp_infores = hit["info"]["x-translator"]["infores"]
    if kp_infores not in sources_by_kps:
        sources_by_kps[kp_infores] = set()
    if kp_infores not in hits_by_infores:
        hits_by_infores[kp_infores] = hit
    if "components" not in hit:
        continue
    for meta_triple in hit["components"]["x-bte-kgs-operations"].values():
        for operation in meta_triple:
            if "source" in operation:
                sources_by_kps[kp_infores].add(operation["source"])

# Build BTE/SP -> KP infores mapping
kp_inforeses = []
for api in bte_list["include"]:
    infores = next(
        (
            hit["info"]["x-translator"]["infores"]
            for hit in smartapi["hits"]
            if hit["_id"] == api["id"]
        ),
        None,
    )
    if infores is not None:
        kp_inforeses.append(infores)

bte_kp = {"infores:biothings-explorer": kp_inforeses}
service_provider_kp = {"infores:service-provider-trapi": kp_inforeses}

# Write out files
with open("data/kps_to_apis.json", "w") as file:
    json.dump({kp: [*sources] for kp, sources in sources_by_kps.items()}, file)
#with open("data/bte_to_kps.json", "w") as file:
#    json.dump({"infores:biothings-explorer": kp_inforeses}, file)
with open("data/sp_to_kps.json", "w") as file:
    json.dump({"infores:service-provider-trapi": kp_inforeses}, file)