
import os
import time
import requests

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("M2M_CLIENT_ID")
CLIENT_SECRET = os.getenv("M2M_CLIENT_SECRET")
AUDIENCE = os.getenv("AUTH0_AUDIENCE")

TOKEN_URL = f"https://{DOMAIN}/oauth/token"
CHAT_URL = "http://127.0.0.1:5000/chat"


def timestamp():
    return datetime.now().astimezone().isoformat(
        timespec="seconds"
    )


print("Starting credential rotation test")

# Step 1: Obtain M2M access token
token_response = requests.post(
    TOKEN_URL,
    json={
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "audience": AUDIENCE,
        "scope": "read:ai-data"
    }
)

if not token_response.ok:
    print("Auth0 Status:", token_response.status_code)
    print("Auth0 Error:", token_response.text)
    raise SystemExit("Token request failed")

token_response.raise_for_status()

token_data = token_response.json()
access_token = token_data["access_token"]
expires_in = int(token_data["expires_in"])

print(f"[{timestamp()}] M2M token obtained")
print(f"Token lifetime: {expires_in} seconds")

if expires_in != 60:
    raise RuntimeError(
        f"Expected 60-second token, received {expires_in} seconds"
    )

headers = {
    "Authorization": f"Bearer {access_token}"
}

# Step 2: First API request
print(f"\n[{timestamp()}] Calling /chat with fresh token")

first_response = requests.post(
    CHAT_URL,
    headers=headers,
    json={"message": "Hello SecureNova AI"}
)

print(
    f"[{timestamp()}] First response: "
    f"{first_response.status_code} "
    f"{first_response.reason}"
)

print(first_response.text)

# Step 3: Wait until token expires
wait_time = expires_in + 3

print(f"\nWaiting {wait_time} seconds for token expiration...")
time.sleep(wait_time)

# Step 4: Replay the same token
print(f"\n[{timestamp()}] Replaying expired token")

second_response = requests.post(
    CHAT_URL,
    headers=headers,
    json={"message": "Replay expired token"}
)

print(
    f"[{timestamp()}] Replay response: "
    f"{second_response.status_code} "
    f"{second_response.reason}"
)

print(second_response.text)

print("\nCredential rotation test completed.")
