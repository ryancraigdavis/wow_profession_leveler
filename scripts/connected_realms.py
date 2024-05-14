import requests
import json

# Array of realm IDs
realm_ids = [121, 127, 151, 115, 106, 1072, 58, 67, 73, 1175, 1184, 1185, 75, 84, 86, 96, 99, 100, 104, 114, 53, 4, 47, 118, 5, 12, 1168, 1171, 1136, 162, 54, 55, 60, 63, 64, 1151, 160, 57, 76, 77, 78, 1425, 1426, 1427, 125, 1070, 1071, 1147, 61, 163, 155, 157, 1129, 1190, 11, 113, 52, 69, 154, 3234, 158, 9, 120, 117, 1138, 71, 1428, 3207, 3208, 3209, 3683, 3684, 3685, 3675, 3676, 3678, 3661, 3693, 3694, 3721, 3723, 3725, 3726]

# Array of classic realm names
classic_realms = realm_names = [
    "Yojamba",
    "Windseeker",
    "Whitemane",
    "Westfall",
    "Sulfuras",
    "Skyfury",
    "Remulos",
    "Pagle",
    "Old Blanchy",
    "Myzrael",
    "Mankrik",
    "Maladath",
    "Grobbulus",
    "Faerlina",
    "Eranikus",
    "Earthfury",
    "Bloodsail Buccaneers",
    "Benediction",
    "Azuresong",
    "Atiesh",
    "Ashkandi",
    "Arugal",
    "Angerforge"
]

# Get the access token from user input
access_token = input("Enter the access token: ")

# Initialize an empty dictionary to store the realm data
realm_data = {}

# Iterate over each realm ID
for realm_id in realm_ids:
    # Construct the API URL
    url = f"https://us.api.blizzard.com/data/wow/connected-realm/{realm_id}?namespace=dynamic-us&locale=en_US&access_token={access_token}"

    try:
        # Send a GET request to the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        # Parse the JSON response
        data = response.json()

        # Extract the realm names from the response
        realms = data["realms"]
        for realm in realms:
            realm_name = realm["name"]
            print(realm_name)
            # Check if the realm name is in the classic_realms array
            if realm_name in classic_realms:
                # Add the realm data to the dictionary
                realm_data[realm_name] = data
                break  # Move on to the next realm ID

    except requests.exceptions.RequestException as e:
        print(f"Error occurred for realm ID {realm_id}: {e}")

# Save the realm data to a JSON file
with open("realm_data.json", "w") as file:
    json.dump(realm_data, file, indent=4)

print("Realm data saved to realm_data.json")
