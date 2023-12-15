
def main():
    import sys
    import os
    import yaml
    import json

    input_file = sys.argv[1]

    def change_file_extension(file_name, new_extension):
        # Split the file name by '.' and replace the last part with the new extension
        base = os.path.splitext(file_name)[0]
        return base + new_extension

    # Read JSON file
    with open(input_file, 'r') as json_file:
        data = json.load(json_file)

    output_file  = change_file_extension(input_file, ".json")

    # Read YAML file
    with open(input_file, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)

    # Convert and save as JSON
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)



if __name__ == "__main__":
    main()