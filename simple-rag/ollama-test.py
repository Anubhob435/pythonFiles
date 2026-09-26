import json
import requests

url = "https://aud-thomas-citizen-inspector.trycloudflare.com/api/generate"
payload = {
    "model": "gemma3:4b",
    "prompt": "Write a 10 line korror story. answer in json structure.",
    "stream": False
}

try:
    response = requests.post(url, json=payload)
    response.raise_for_status()

    try:
        data = response.json()
    except json.JSONDecodeError:
        # Fallback for NDJSON / streaming lines
        lines = [line.strip() for line in response.text.strip().splitlines() if line.strip()]
        data = json.loads(lines[-1])

    if isinstance(data, dict) and "response" in data:
        print(data["response"])
    else:
        print(data)
except Exception as e:
    print(f"Error making request: {e}")

