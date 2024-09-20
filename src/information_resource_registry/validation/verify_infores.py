import os
import time
import random
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
    total=3,  # Reduce the number of retries to avoid hammering sites
    backoff_factor=1,  # Backoff factor for retries
    status_forcelist=[500, 502, 503, 504],  # Retry on these status codes
)

# Use a global http PoolManager for reuse across requests
http = urllib3.PoolManager(ssl_context=ctx,
                           retries=retry_strategy,
                           timeout=urllib3.util.Timeout(connect=10, read=30))

def is_valid_url(urls: str) -> bool:
    for url in urls:
        print(f"Validating URL: {url}")
        try:
            # Add a randomized sleep to avoid rapid requests
            time.sleep(random.uniform(1, 3))
            response = http.request("GET", url, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status == 200:
                return True
            else:
                return False
        except urllib3.exceptions.RequestError as e:
            print(f"Request error: {e}")
            print(f"URL: {url}")
            return False  # Consider the URL invalid if there's a request error

class InformationResource:

    def __init__(self) -> None:
        self.infores_map = {}

    def dump(self):
        raise NotImplementedError

    def validate(self):
        with open(INFORES_YAML, 'r') as yaml_file:
            data = yaml.safe_load(yaml_file)
            for infores in data.get('information_resources'):
                if infores.get("status") == "deprecated":
                    continue

                # Validation for status
                if infores.get("status") not in ["released", "deprecated", "draft", "modified"]:
                    print(infores)
                    raise ValueError(f"Invalid infores status: {infores.get('status')} for {infores.get('name')}")

                # Validation for knowledge level
                if infores.get("knowledge_level") not in ["knowledge_assertion", "statistical_association",
                                                          "prediction", "observation", "not_provided",
                                                          "logical_entailment", "mixed", "other"]:
                    print(infores)
                    raise ValueError(f"Invalid knowledge level: {infores.get('knowledge_level')} for {infores.get('name')}")

                # Validation for agent type
                if infores.get("agent_type") not in ["manual_agent", "not_provided", "automated_agent",
                                                     "data_analysis_pipeline", "computational_model",
                                                     "text_mining_agent", "image_processing_agent",
                                                     "manual_validation_of_automated_agent"]:
                    print(infores)
                    raise ValueError(f"Invalid agent type: {infores.get('agent_type')} for {infores.get('name')}")

                # Exceptions or URL validation
                if infores.get("id") in ['infores:athena', 'infores:isb-wellness', 'infores:isb-incov',
                                         'infores:preppi', 'infores:ttd', 'infores:flybase', 'infores:xenbase',
                                         'infores:aeolus', 'infores:ctrp', 'infores:date', 'infores:mirbase',
                                         'infores:nsides', 'infores:irefindex', 'infores:kinomescan',
                                         'infores:community-sar', 'infores:omicsdi', 'infores:ndcd',
                                         'infores:atc-codes-umls'] or infores.get("xref") is None \
                        or infores.get("status") == 'deprecated' or is_valid_url(infores.get("xref")):
                    print(f"{infores.get('id')} has valid URL")
                else:
                    print(infores)
                    raise ValueError(f"Invalid infores URL for {infores.get('name')}")

if __name__ == "__main__":
    InformationResource().validate()

