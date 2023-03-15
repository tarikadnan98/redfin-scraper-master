import json
import csv
import time
from haralyzer import HarParser
import tkinter as tk
from tkinter import filedialog

# Prompt User to upload the HAR file from local machine
# Below block of codes get the HAR file as input and convert it into a json

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

# Load the HAR file
with open(file_path, 'r', encoding='utf-8') as f:
    har_parser = HarParser(json.loads(f.read()))

# Convert the HAR file to JSON
json_data = har_parser.har_data

# Write the JSON output to a file, change the file name accordingly
with open('Moore_Raw.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)


# Now the first converted json file is parsed and grouped based upon the filter  "https://www.redfin.com/stingray/api/gis?"
# Also, make a second json file which will contain only the response block that contains the actual home data we need
# Add a 5-second delay in case the first json creation time is high

time.sleep(8)

with open("Moore_Raw.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

matching_responses = []

for entry in data['entries']:
    request_url = entry['request']['url']
    if "https://www.redfin.com/stingray/api/gis?" in request_url:
        matching_responses.append(entry['response'])

output_data = {'responses': matching_responses}

# Write the JSON output to a file, change the file name accordingly

with open('Moore_Redfin_Grouped.json', 'w') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

time.sleep(8)

# Below code block will now take the latest json file and sanitize as your desired data is inside a block
# and formatting is bad to parse

# Open the JSON file and read its contents

with open('Moore_Redfin_Grouped.json', 'r', encoding='utf-8') as file:
    json_data = file.read()

# Parse the JSON data
parsed_data = json.loads(json_data)

# Access the parsed data and sanitize the backslash and unnecessary
matching_responses = []
for entry in parsed_data['responses']:
    json_parsed = entry['content']['text'].replace('{}&&', '').replace('\\', '')
    matching_responses.append(json_parsed)

# Write the JSON output to a file, change the file name accordingly
with open('Moore_Redfin_Grouped_Sanitized.json', 'w') as file:
    file.write(json_parsed)

# Add a 5-second delay
time.sleep(8)

with open('Moore_Redfin_Grouped_Sanitized.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract all prices from the latest json

homes = data['payload']['homes']
rows = []
for home in homes:
    price = home.get('price', '').get('value', '')
    zip_code = home.get('zip', '')
    property_id = home.get('propertyId', '')
    url = home.get('url', '')
    listingRemarks = home.get('listingRemarks', '')
    lotSize = home.get('lotSize').get('value', '')
    lastSaleDate = home.get('sashes')[0].get('lastSaleDate', '')
    latitude = home.get('latLong').get('value').get('latitude', '')
    longitude = home.get('latLong').get('value').get('longitude', '')
    rows.append([price, zip_code, property_id, "https://www.redfin.com"+url, listingRemarks, lotSize/43560, lastSaleDate, latitude, longitude])

# Write the data to a CSV file
with open('Moore_Redfin_Output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Sale Price', 'Zip Code', 'ID', 'URL', 'Descriptions', 'Acreage', 'Sale Date', 'Latitude', 'Longitude'])
    writer.writerows(rows)
