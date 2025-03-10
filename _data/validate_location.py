import yaml

# Function to read YAML file
def read_yaml_file(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Path to the YAML file
file_path = 'enseignes.yml'

# Read the YAML content from the file
data = read_yaml_file(file_path)
# Get the list of allowed cities
allowed_cities = data.get('allowed_cities', [])

# Validate each enseigne's location
for enseigne_name, enseigne_details in data.get('enseignes', {}).items():
    location = enseigne_details.get('city')
    if location not in allowed_cities:
        print(f"Validation Error: {enseigne_name} has an invalid city: {location}")
    # else:
    #     print(f"{enseigne_name} has a valid city: {location}")