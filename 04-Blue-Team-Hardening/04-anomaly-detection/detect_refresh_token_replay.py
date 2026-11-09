import os
import requests
from dotenv import load_dotenv

load_dotenv(r"C:\Auth0-PKCE\.env")

domain = os.getenv("AUTH0_DOMAIN")
client_id = os.getenv("M2M_CLIENT_ID")
client_secret = os.getenv("M2M_CLIENT_SECRET")

if not all([domain, client_id, client_secret]):
    raise RuntimeError("Missing Auth0 credentials.")

base_url = f"https://{domain}"

# Get Management API token
response = requests.post(
    f"{base_url}/oauth/token",
    json={
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": f"{base_url}/api/v2/",
        "grant_type": "client_credentials"
    },
    timeout=20
)
response.raise_for_status()
token = response.json()["access_token"]

# Fetch recent Auth0 logs
response = requests.get(
    f"{base_url}/api/v2/logs",
    headers={"Authorization": f"Bearer {token}"},
    params={"per_page": 100, "sort": "date:-1"},
    timeout=30
)
response.raise_for_status()
logs = response.json()

print("LIVE AUTH0 REFRESH-TOKEN REPLAY DETECTION")
print(f"Events scanned: {len(logs)}")

detected = 0

for log in logs:
    description = log.get("description", "").lower()

    if "reused refresh token" in description:
        detected += 1
        print("\nSECURITY ALERT: REFRESH-TOKEN REPLAY DETECTED")
        print("Date:", log.get("date"))
        print("IP:", log.get("ip", "unknown"))
        print("Event:", log.get("type"))
        print("Description:", log.get("description"))

if detected:
    print(f"\nRESULT: PASSED - {detected} replay event(s) detected.")
else:
    print("\nNo refresh-token replay event found in the latest 100 logs.")
