import json
from haralyzer import HarParser

# Load the HAR file
with open('c:/Moore.har', 'r', encoding='utf-8') as f:
    har_parser = HarParser(json.loads(f.read()))

# Convert the HAR file to JSON
json_data = har_parser.har_data

# Save the JSON data to a file
with open('Moore_Raw.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)
