import requests
import os

url = "https://www.cde.ca.gov/SchoolDirectory/active-or-pending-schools/2/0/1/500"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

# Make request with timeout
try:
    print(f"Fetching: {url}")
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()  # Raise exception for bad status codes
    print(f"Status Code: {response.status_code}")
except requests.exceptions.Timeout:
    print("Error: Request timed out after 30 seconds")
    exit(1)
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    exit(1)

# Get current script directory
folder = os.path.dirname(os.path.abspath(__file__))

# File path
file_path = os.path.join(folder, "response.html")

# Save HTML
with open(file_path, "w", encoding="utf-8") as f:
    f.write(response.text)

print(f"Saved HTML to: {file_path}")
print(f"Content length: {len(response.text)} characters")