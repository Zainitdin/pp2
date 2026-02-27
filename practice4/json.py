# Import json module
# It is used to work with JSON files in Python
import json


# Open the file "sample-data.json" in read mode
# 'with' automatically closes the file after reading
with open("sample-data.json") as f:
    # json.load() converts JSON data into Python dictionary
    data = json.load(f)


# Print table title
print("Interface Status")

# Print line separator
print("=" * 79)

# Print table headers with formatting
# <50 means left alignment with width of 50 characters
print(f"{'DN':<50} {'Description':<20} {'Speed':<6} {'MTU':<6}")

# Print underline for headers
print("-" * 50 + " " + "-" * 20 + " " + "-" * 6 + " " + "-" * 6)


# Loop through each item in the JSON data
# data["imdata"] accesses the main list in the JSON structure
for item in data["imdata"]:
    
    # Access nested dictionary:
    # l1PhysIf → attributes
    attr = item["l1PhysIf"]["attributes"]
    
    # Safely get values from dictionary
    # .get() prevents errors if key does not exist
    dn = attr.get("dn", "")
    descr = attr.get("descr", "")
    speed = attr.get("speed", "")
    mtu = attr.get("mtu", "")
    
    # Print formatted row
    print(f"{dn:<50} {descr:<20} {speed:<6} {mtu:<6}")