
def main():
    import sys
    import os
    import json
    import yaml

    input_file = sys.argv[1] 

    def change_file_extension(file_name, new_extension) -> str:
        # Split the file name by '.' and replace the last part with the new extension
        base = os.path.splitext(file_name)[0]
        return base + new_extension

    # Read JSON file
    with open(input_file, 'r') as json_file:
        data = json.load(json_file)

    output_file  = change_file_extension(input_file, ".yaml")
    # Convert and save as YAML
    with open(output_file, 'w') as yaml_file:
        yaml.dump(data, yaml_file)


if __name__ == "__main__":
    main()