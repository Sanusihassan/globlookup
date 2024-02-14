"""
 i have a json file on ../store/country_codes.json that looks somthing like this:
 {
    "Afghanistan": "93",
    "Åland": "358 (18)",
    "Albania": "355",
    "Algeria": "213",
    "American Samoa": "1 (684)",
    "Andorra": "376",
    "Angola": "244",
    "Anguilla": "1 (264)",....}
    i want to create a json folder in the store folder and create an empty json file for each entry i.e create files like Afghanistan.json and so on.
"""

import os
import json

# Path to the original JSON file
original_file_path = '/workspace/globlookup/backend/store/country_codes.json'

# Create a directory to store the new JSON files
output_dir = 'store/json'
os.makedirs(output_dir, exist_ok=True)

# Read the original JSON file
with open(original_file_path, 'r') as file:
    country_codes = json.load(file)

# Create an empty JSON file for each country code
for country, code in country_codes.items():
    file_path = os.path.join(output_dir, f"{country}.json")
    with open(file_path, 'w') as outfile:
        json.dump({}, outfile, indent=4)
        print(f"Created empty JSON file for {country} at {file_path}")
