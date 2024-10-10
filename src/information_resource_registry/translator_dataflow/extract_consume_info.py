import yaml
import csv
import sys

def parse_and_write_csv(yaml_file_path, csv_file_path):
    # Read the YAML file
    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)

    # Prepare the CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['ID', 'Consumed By', 'Value'])

        # Process each resource in the YAML data
        for resource in data['information_resources']:
            # Extract the ID and check if consumed_by exists
            resource_id = resource['id']
            if 'consumed_by' in resource:
                # Write each consumed_by entry as a new row
                for consumed_by in resource['consumed_by']:
                    writer.writerow([resource_id, consumed_by, '1'])

    print(f"CSV file created at {csv_file_path}")

def main():
    if len(sys.argv) != 3:
        print("Usage: parse_and_write_csv <input_yaml_file_path> <output_csv_file_path>")
        sys.exit(1)
    input_yaml_path = sys.argv[1]
    output_csv_path = sys.argv[2]
    parse_and_write_csv(input_yaml_path, output_csv_path)

if __name__ == "__main__":
    main()