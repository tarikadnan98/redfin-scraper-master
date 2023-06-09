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
file_path_grouped = os.path.join(folder_path, folder_name + "_Redfin_Grouped.json")
file_path_sanitized = os.path.join(folder_path, folder_name + "_Redfin_Grouped_Sanitized.json")
file_path_csv = os.path.join(folder_path, folder_name + "_Redfin_Output.csv")
file_path_csv_final = os.path.join(folder_path, folder_name + "_Redfin_Output_Final_All_Property.csv")
file_path_csv_final_with_public_record_removed = os.path.join(folder_path, folder_name + "_Redfin_Sold_Comps_PublicRecord_Removed.csv")

with open(file_path_raw, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)
