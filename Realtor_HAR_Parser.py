import os
import tkinter as tk
from tkinter import simpledialog, filedialog
import json
import csv
import time
from haralyzer import HarParser
import pandas as pd


# Prompt the user to select a folder location
root = tk.Tk()
root.withdraw()
folder_location = filedialog.askdirectory()

# Prompt the user to enter the folder name
folder_name = simpledialog.askstring("Input", "Enter folder name", parent=root)

# Check if the folder name is valid
if folder_name is None or len(folder_name.strip()) == 0:
    print("Invalid folder name")
else:
    # Check if the folder location exists
    if not os.path.isdir(folder_location):
        print("Invalid folder location")
    else:
        # Create the folder in the specified location
        folder_path = os.path.join(folder_location, folder_name)
        os.mkdir(folder_path)
        print("Folder created at:", folder_path)

# Below this
file_path = filedialog.askopenfilename()

# Load the HAR file
with open(file_path, 'r', encoding='utf-8') as f:
    har_parser = HarParser(json.loads(f.read()))

# Convert the HAR file to JSON
json_data = har_parser.har_data

# Write the JSON output to a file, change the file name accordingly

file_path_raw = os.path.join(folder_path, folder_name + "_Raw.json")
file_path_grouped = os.path.join(folder_path, folder_name + "_Realtor_Grouped.json")
file_path_sanitized = os.path.join(folder_path, folder_name + "_Realtor_Grouped_Sanitized.json")
file_path_csv = os.path.join(folder_path, folder_name + "_Realtor_Output.csv")
file_path_csv_final = os.path.join(folder_path, folder_name + "_Realtor_Output_Final_All_Property.csv")
file_path_csv_final_with_public_record_removed = os.path.join(folder_path, folder_name + "_Realtor_Sold_Comps_PublicRecord_Removed.csv")

with open(file_path_raw, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)


# Now the first converted json file will be parsed and grouped based upon the filter  "https://www.realtor.com/api/v1/hulk_main_srp?"
# Also, make a second json file which will contain only the response block that contains the actual home data we need
# Add a 5-second delay in case the first json creation time is high

time.sleep(8)

with open(file_path_raw, 'r', encoding='utf-8') as f:
    data = json.load(f)

matching_responses = []

for entry in data['entries']:
    request_url = entry['request']['url']
    if "https://www.realtor.com/api/v1/hulk_main_srp?" in request_url:
        matching_responses.append(entry['response'])

output_data = {'responses': matching_responses}

# Write the JSON output to a file, change the file name accordingly

with open(file_path_grouped, 'w') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)\

time.sleep(8)

# Below code block will now take the latest json file and sanitize

# Open the JSON file and read its contents

with open(file_path_grouped, 'r', encoding='iso-8859-1') as f:
    json_data = json.load(f)

# Access the parsed data and sanitize the backslash and unnecessary characters
matching_responses = []
for entry in json_data['responses']:
    json_parsed = entry['content']['text'].replace('{}&&', '')
    matching_responses.append(json.loads(json_parsed))

# Write the JSON output to a file, change the file name accordingly
with open(file_path_sanitized, "w") as file:
    json.dump(matching_responses, file)

# ##########

# Add a 5-second delay
time.sleep(5)

with open(file_path_sanitized, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract all the necessary values from the latest json

with open(file_path_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # write header row
    writer.writerow(['Sold Price', 'County',  'Zip Code', 'Data Source ID', 'Property ID', 'URL', 'Acreage', 'Sold Date', 'Latitude', 'Longitude'])
    for obj in data:
        try:
            homes = obj['data']['home_search']['results']
        except KeyError:
            # Skip this object and continue with the next one
            continue
        for home in homes:
            price = home.get('description').get('sold_price', '')
            zip_code = home.get('location').get('address').get('postal_code', '')
            county = home.get('location').get('county').get('name', '')
            data_source = home.get('source')
            if data_source is not None:
                dataSource_Id = data_source.get('id', '')
            else:
                dataSource_Id = ''
            property_id = home.get('property_id', '')
            url = home.get('permalink', '')
            lotSize = home.get('description').get('lot_sqft', '')
            lastSaleDate = home.get('description').get('sold_date', '')
            latitude = home.get('location').get('address').get('coordinate').get('lat', '')
            longitude = home.get('location').get('address').get('coordinate').get('lon', '')
            lot_size_acres = lotSize / 43560 if lotSize else ""
            lot_size_acres_formatted = "{:.2f}".format(lot_size_acres) if isinstance(lot_size_acres, float) else ""
            writer.writerow([price, county, zip_code, dataSource_Id, property_id, "https://www.realtor.com/realestateandhomes-detail/"+url, lot_size_acres_formatted, lastSaleDate, latitude, longitude])


time.sleep(5)
# Load the CSV file
df = pd.read_csv(file_path_csv)

# Remove duplicates based on the 'propertyId' column
df.drop_duplicates(subset=['URL'], keep='first', inplace=True)

# Save the result to a new CSV file
df.to_csv(file_path_csv_final, index=False)

# time.sleep(5)
# # drop rows based on a column value
#
# df = pd.read_csv(file_path_csv_final)
#
# # drop rows where the Data Source ID value is equal to '13'. dataSourceId=13 means the property source is from Public Record
# # and Public Record source data is considered as Outlier. So, those properties need to be removed from the csv
#
# df = df.drop(df[df['Data Source ID'] == 13].index)
#
# # Save the result to a new CSV file
# df.to_csv(file_path_csv_final_with_public_record_removed, index=False)
