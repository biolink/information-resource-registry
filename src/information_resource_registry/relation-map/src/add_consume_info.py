from ruamel.yaml import YAML
import json
import sys

yaml = YAML()
yaml.indent(sequence=4, offset=2)

# Retrieve file paths from command line arguments
yaml_file_path = sys.argv[1]
json_file_paths = sys.argv[2:]  # List of JSON file paths

# Process each JSON file and consolidate updates into a single dictionary
update_data = {}
for json_file_path in json_file_paths:
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)
    for key, new_values in json_data.items():
        if key not in update_data:
            update_data[key] = {'consumes': set(), 'consumed_by': set()}
        update_data[key]['consumes'].update(new_values)
        for value in new_values:
            if value not in update_data:
                update_data[value] = {'consumes': set(), 'consumed_by': set()}
            update_data[value]['consumed_by'].add(key)

# Load the existing YAML data
with open(yaml_file_path, 'r') as file:
    data = yaml.load(file)
    yaml_data = data['information_resources']

# Update the YAML data based on the consolidated JSON data
for resource in yaml_data:
    resource_id = resource['id']
    if resource_id in update_data:
        if update_data[resource_id]['consumes']:
            if 'consumes' not in resource:
                resource['consumes'] = []
            resource['consumes'].extend(list(update_data[resource_id]['consumes'] - set(resource['consumes'])))
        if update_data[resource_id]['consumed_by']:
            if 'consumed_by' not in resource:
                resource['consumed_by'] = []
            resource['consumed_by'].extend(list(update_data[resource_id]['consumed_by'] - set(resource['consumed_by'])))

# Add new entries to yaml_data if they don't exist
for key, values in update_data.items():
    if not any(res['id'] == key for res in yaml_data):
        new_entry = {'id': key}
        if values['consumes']:
            new_entry['consumes'] = list(values['consumes'])
        if values['consumed_by']:
            new_entry['consumed_by'] = list(values['consumed_by'])
        yaml_data.append(new_entry)

# infores catalog starts with this line
print("---")

# Output the updated YAML data to STDOUT with specific formatting
yaml.width = 90
yaml.dump(data, sys.stdout)

