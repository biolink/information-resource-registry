#!/usr/bin/env python3
"""Sync knowledge_level and agent_type data from RTX-KG2 to infores_catalog.yaml"""

import sys
from pathlib import Path
import requests
from ruamel.yaml import YAML

# URLs
RTX_KG2_MAP_URL = "https://raw.githubusercontent.com/RTXteam/RTX-KG2/refs/heads/master/maps/knowledge-level-agent-type-map.yaml"
INFORES_CATALOG_PATH = Path("infores_catalog.yaml")

def main():
    # Load RTX-KG2 data
    print(f"Fetching RTX-KG2 data from {RTX_KG2_MAP_URL}...")
    response = requests.get(RTX_KG2_MAP_URL)
    response.raise_for_status()

    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 88
    yaml.explicit_start = True
    yaml.indent(mapping=4, sequence=4, offset=2)
    yaml.default_flow_style = False
    yaml.representer.ignore_aliases = lambda *_: True

    rtx_data = yaml.load(response.text)

    # Load our infores catalog
    print(f"Loading {INFORES_CATALOG_PATH}...")
    with INFORES_CATALOG_PATH.open() as f:
        catalog = yaml.load(f)

    # Track updates
    updated_count = 0
    not_found_count = 0
    not_found_ids = []

    # Update each infores entry
    for infores_id, rtx_info in rtx_data.items():
        # Find the corresponding entry in our catalog
        found = False
        for resource in catalog["information_resources"]:
            if resource.get("id") == infores_id:
                found = True
                old_agent = resource.get("agent_type")
                old_knowledge = resource.get("knowledge_level")
                new_agent = rtx_info.get("agent_type")
                new_knowledge = rtx_info.get("knowledge_level")

                # Update if different
                if old_agent != new_agent or old_knowledge != new_knowledge:
                    print(f"Updating {infores_id}:")
                    if old_agent != new_agent:
                        print(f"  agent_type: {old_agent} -> {new_agent}")
                        resource["agent_type"] = new_agent
                    if old_knowledge != new_knowledge:
                        print(f"  knowledge_level: {old_knowledge} -> {new_knowledge}")
                        resource["knowledge_level"] = new_knowledge
                    updated_count += 1
                break

        if not found:
            not_found_count += 1
            not_found_ids.append(infores_id)

    print(f"\nSummary:")
    print(f"  Updated: {updated_count} entries")
    print(f"  Not found in catalog: {not_found_count} entries")

    if not_found_ids:
        print(f"\nEntries in RTX-KG2 but not in catalog:")
        for infores_id in sorted(not_found_ids):
            print(f"  - {infores_id}")

    if updated_count > 0:
        # Write back to file
        print(f"\nWriting updates to {INFORES_CATALOG_PATH}...")
        with INFORES_CATALOG_PATH.open("w") as f:
            yaml.dump(catalog, f)
        print("Done!")
    else:
        print("\nNo updates needed.")

    return 0

if __name__ == "__main__":
    sys.exit(main())
