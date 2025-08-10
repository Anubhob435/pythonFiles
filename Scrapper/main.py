import requests
import json

# Base URL for the FeatureServer layer containing recycling infrastructure
BASE_URL = "https://services.arcgis.com/cJ9YHowT8TU7DUyn/arcgis/rest/services/High-volume_Recycling_Infrastructure/FeatureServer/3/query"

# Query parameters to get ALL features in JSON with lat/long
params = {
    "where": "1=1",        # Select all rows
    "outFields": "*",      # Get all columns
    "outSR": "4326",       # WGS84 lat/lon
    "f": "json"            # Output format
}

print("[*] Fetching recycling infrastructure data...")
response = requests.get(BASE_URL, params=params)

if response.status_code != 200:
    print(f"[!] Failed to fetch data: HTTP {response.status_code}")
    exit()

data = response.json()
features = data.get("features", [])

print(f"[*] Found {len(features)} facilities\n")

# Build a clean list of facilities with coordinates and all details
facilities_list = []
for feature in features:
    attrs = feature.get("attributes", {})
    geom = feature.get("geometry", {})

    facility_data = {
        "name": attrs.get("Name", "Unknown Facility"),
        "coordinates": {
            "latitude": geom.get("y"),
            "longitude": geom.get("x")
        },
        "details": attrs
    }
    facilities_list.append(facility_data)

# Save everything in one JSON file
with open("recycling_infrastructure.json", "w", encoding="utf-8") as f:
    json.dump(facilities_list, f, ensure_ascii=False, indent=2)

print(f"[+] All facility data saved to recycling_infrastructure.json")
