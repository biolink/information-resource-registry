import os
import requests
import csv
import time
import urllib3
from urllib3.util.ssl_ import create_urllib3_context
from urllib3.util.retry import Retry
import yaml

ctx = create_urllib3_context()
ctx.load_default_certs()
ctx.options |= 0x4  # ssl.OP_LEGACY_SERVER_CONNECT

INFORES_YAML = os.path.join('infores_catalog.yaml')

from urllib3.poolmanager import PoolManager

# Define retry strategy
retry_strategy = Retry(
    total=5,  # Number of retries
    backoff_factor=1,  # Backoff factor for retries
    status_forcelist=[500, 502, 503, 504],  # Retry on these status codes
)


def is_valid_url(urls: str) -> bool:
    for url in urls:
        try:
            with urllib3.PoolManager(ssl_context=ctx,
                                        retries=retry_strategy,
                                        timeout=urllib3.util.Timeout(connect=10, read=30)) as http:
                response = http.request("GET", url, headers={'User-Agent': 'Mozilla/5.0'})
                if response.status == 200:
                    return True
                else:
                    return False
        except requests.exceptions.RequestException as e:
            print(url)


class InformationResource:

    def __init__(self) -> None:
        infores_map = {}

    def dump(self):
        raise NotImplementedError

    def validate(self):
        with open(INFORES_YAML, 'r') as yaml_file:
            data = yaml.safe_load(yaml_file)
            for infores in data.get('information_resources'):
                # exceptions for resolvable URLs that don't return 200 response for some reason (e.g. require
                # user to accept a popup before resolving):
                if infores.get("status") == "deprecated":
                    continue
                if infores.get("status") not in ["released", "deprecated", "draft", "modified"]:
                    print(infores)
                    print("Invalid infores status:" + infores.get("status")
                          + " for " + infores.get("name"))
                    raise ValueError("invalid status for " + infores.get("name") + " for " + infores.get("id"))
                if infores.get("knowledge_level") not in ["knowledge_assertion",
                                                          "statistical_association",
                                                          "prediction",
                                                          "observation",
                                                          "not_provided",
                                                          "logical_entailment",
                                                          "mixed",
                                                          "other"]:
                    print(infores)
                    print("Invalid infores knowledge level:" + infores.get("knowledge_level")
                          + " for " + infores.get("name"))
                    raise ValueError("invalid knowledge level for " + infores.get("name") + " for " + infores.get("id"))

                if infores.get("agent_type") not in ["manual_agent",
                                                     "not_provided",
                                                     "automated_agent",
                                                     "data_analysis_pipeline",
                                                     "computational_model",
                                                     "text_mining_agent",
                                                     "image_processing_agent",
                                                     "manual_validation_of_automated_agent"]:
                    print(infores)
                    print("Invalid infores agent type:" + infores.get("agent_type") + " for " + infores.get("name"))
                    raise ValueError("invalid agent type for " + infores.get("name") + " for " + infores.get("id"))

                if infores.get("id") == 'infores:athena' \
                        or infores.get("id") == 'infores:isb-wellness' \
                        or infores.get("id") == 'infores:isb-incov' \
                        or infores.get("id") == 'infores:preppi' \
                        or infores.get("id") == 'infores:ttd' \
                        or infores.get("id") == 'infores:flybase' \
                        or infores.get("id") == 'infores:xenbase' \
                        or infores.get("id") == 'infores:aeolus' \
                        or infores.get("id") == 'infores:ctrp' \
                        or infores.get("id") == 'infores:date' \
                        or infores.get("id") == "infores:mirbase" \
                        or infores.get("id") == "infores:nsides" \
                        or infores.get("id") == "infores:irefindex" \
                        or infores.get("id") == "infores:kinomescan" \
                        or infores.get("id") == "infores:community-sar" \
                        or infores.get("id") == "infores:omicsdi" \
                        or infores.get("id") == "infores:atc-codes-umls" \
                        or infores.get("xref") is None \
                        or infores.get("status") == 'deprecated' \
                        or is_valid_url(infores.get("xref")):
                    print(infores.get('id'), "has valid URL")
                else:
                    print(infores)
                    print("Invalid infores URL:" + " for " + infores.get("name"))
                    raise ValueError("invalid URL" + infores.get("name") + " for " + infores.get("id"))


if __name__ == "__main__":
    InformationResource().validate()
