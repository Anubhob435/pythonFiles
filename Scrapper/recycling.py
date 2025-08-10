import requests
import json

# Base query URL for EPA Disaster Debris Recovery Data — replace layer index if needed
BASE_URL = "https://services.arcgis.com/cJ9YHowT8TU7DUyn/arcgis/rest/services/EPA_Disaster_Debris_Recovery_Data/FeatureServer/0/query"

def fetch_all_features():
    all_features = []
    offset = 0
    page_size = 1000  # adjust if necessary based on server limits

    while True:
        params = {
            "where": "1=1",
            "outFields": "*",
            "outSR": "4326",
            "f": "json",
            "resultOffset": offset,
            "resultRecordCount": page_size
        }

        resp = requests.get(BASE_URL, params=params)
        resp.raise_for_status()
        result = resp.json()

        features = result.get("features", [])
        all_features.extend(features)

        print(f"Fetched {len(features)} records (offset {offset}).")

        # If Laid returned fewer than requested OR no flag, assume done
        if not result.get("exceededTransferLimit") or len(features) < page_size:
            break

        offset += page_size

    return all_features

def build_clean_list(features):
    clean = []
    for feature in features:
        attrs = feature.get("attributes", {})
        lat = attrs.get("Latitude")
        lon = attrs.get("Longitude")

        entry = {
            "name": attrs.get("Company") or attrs.get("Address") or f"Facility_{attrs.get('OBJECTID')}",
            "coordinates": {"latitude": lat, "longitude": lon},
            "details": attrs
        }
        clean.append(entry)
    return clean

def main():
    print("[*] Starting data fetch...")
    features = fetch_all_features()
    print(f"[*] Total records fetched: {len(features)}")

    facilities = build_clean_list(features)
    with open("recycling_infrastructure_all.json", "w", encoding="utf-8") as f:
        json.dump(facilities, f, ensure_ascii=False, indent=2)
    print("[+] Saved all facility information to recycling_infrastructure_all.json")

if __name__ == "__main__":
    main()
