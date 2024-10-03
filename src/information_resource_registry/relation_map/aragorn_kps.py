import asyncio
import json
from kp_registry import Registry

infores_dict = {"infores:aragorn": []}


async def main():
    registry = Registry()

    kps = await registry.retrieve_kps()

    for kp in kps.values():
        if kp.get("maturity") == "staging":
            infores_dict["infores:aragorn"].append(kp.get("infores", "Unknown"))
    
    # Sort the list in alphabetical order
    infores_dict['infores:aragorn'].sort()

    with open('src/information_resource_registry/relation_map/data/aragorn_to_kps.json', 'w') as outfile:
        json.dump(infores_dict, outfile, indent=2, sort_keys=True)

if __name__ == "__main__":
    asyncio.run(main())
