import os
import requests
from datetime import datetime, timezone, timedelta
from collections import defaultdict, Counter
from dotenv import load_dotenv

load_dotenv(r"C:\Auth0-PKCE\.env")

DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("M2M_CLIENT_ID")
CLIENT_SECRET = os.getenv("M2M_CLIENT_SECRET")

if not all([DOMAIN, CLIENT_ID, CLIENT_SECRET]):
    raise RuntimeError("Missing Auth0 Management API credentials.")

BASE_URL = f"https://{DOMAIN}"
TOKEN_URL = f"{BASE_URL}/oauth/token"
LOGS_URL = f"{BASE_URL}/api/v2/logs"

def get_management_token():
    response = requests.post(
        TOKEN_URL,
        json={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "audience": f"{BASE_URL}/api/v2/",
            "grant_type": "client_credentials"
        },
        timeout=20
    )
    response.raise_for_status()
    return response.json()["access_token"]

def fetch_logs(token):
    response = requests.get(
        LOGS_URL,
        headers={"Authorization": f"Bearer {token}"},
        params={
            "per_page": 100,
            "sort": "date:-1"
        },
        timeout=30
    )
    response.raise_for_status()
    return response.json()

def detect_anomalies(logs):
    failed_by_ip = defaultdict(list)
    replay_events = []
    unfamiliar_ips = set()

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(minutes=10)

    for log in logs:
        ip = log.get("ip", "unknown")
        event_type = log.get("type", "")
        date = log.get("date", "")

        try:
            event_time = datetime.fromisoformat(
                date.replace("Z", "+00:00")
            )
        except (ValueError, AttributeError):
            continue

        if event_type in {"fp", "f"} and event_time >= cutoff:
            failed_by_ip[ip].append(log)

        description = log.get("description", "").lower()
        if "reused refresh token" in description:
            replay_events.append(log)

        if ip != "unknown":
            unfamiliar_ips.add(ip)

    print("\n========== LIVE AUTH0 ANOMALY REPORT ==========")
    print(f"Real Auth0 events retrieved: {len(logs)}")

    print("\n1. Failed authentication attempts")
    alerts = 0
    for ip, events in failed_by_ip.items():
        if len(events) >= 5:
            print(f"ALERT: {len(events)} failures from IP {ip}")
            alerts += 1

    if alerts == 0:
        print("No repeated-failure threshold detected.")

    print("\n2. Refresh-token replay")
    if replay_events:
        for event in replay_events:
            print(
                "ALERT: Refresh-token replay rejected",
                "| Date:", event.get("date"),
                "| IP:", event.get("ip", "unknown")
            )
    else:
        print("No refresh-token replay event found in retrieved logs.")

    print("\n3. Source IP visibility")
    print(f"Distinct IP addresses in retrieved logs: {len(unfamiliar_ips)}")
    for ip in sorted(unfamiliar_ips):
        print("Observed IP:", ip)

    print("\nNOTE: Observed IPs are not automatically classified as malicious.")
    print("================================================")

def main():
    print("Connecting to Auth0 Management API...")
    token = get_management_token()
    print("Management API authentication successful.")

    logs = fetch_logs(token)
    print("Live Auth0 log retrieval successful.")

    detect_anomalies(logs)

if __name__ == "__main__":
    main()
