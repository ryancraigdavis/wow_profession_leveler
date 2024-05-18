import re
import json

# Read the item class data from the JSON file
with open('item_classes.json') as f:
    item_class_data = json.load(f)

# Create a dictionary to store the item class and subclass names
class_names = {}
subclass_names = {}

for item_class in item_class_data:
    class_id = item_class['class_id']
    class_name = item_class['name']
    class_names[class_id] = class_name
    
    if 'item_subclasses' in item_class:
        for subclass in item_class['item_subclasses']:
            subclass_id = subclass['id']
            subclass_name = subclass['name']
            subclass_names[(class_id, subclass_id)] = subclass_name

# Read the raw item data from the Lua file
with open('raw_item_id.lua', 'r') as f:
    lua_content = f.read()

# Extract the item data using regular expressions
pattern = r'\[(\d+)\] = {\'(.*?)\',.*?(\d+),(\d+)}'
matches = re.findall(pattern, lua_content)

# Create a list to store the processed item data
processed_items = []

for match in matches:
    item_id = int(match[0])
    item_name = match[1]
    class_id = int(match[2])
    subclass_id = int(match[3])
    
    class_name = class_names.get(class_id, 'Unknown')
    subclass_name = subclass_names.get((class_id, subclass_id), 'Unknown')
    
    item_data = {
        'item_id': item_id,
        'item_name': item_name,
        'item_class': {
            'id': class_id,
            'name': class_name
        },
        'item_subclass': {
            'id': subclass_id,
            'name': subclass_name
        }
    }
    
    processed_items.append(item_data)

# Write the processed item data to a new JSON file
with open('item_id_classes.json', 'w') as f:
    json.dump(processed_items, f, indent=4)
