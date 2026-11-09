import os
import secrets
import threading
import webbrowser
from urllib.parse import urlencode

import requests
from flask import Flask, request, redirect, session
from dotenv import load_dotenv

load_dotenv(r"C:\Auth0-PKCE\.env")

DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("SSO_CLIENT_ID")
CLIENT_SECRET = os.getenv("SSO_CLIENT_SECRET")
AUDIENCE = os.getenv("AUTH0_AUDIENCE")
CALLBACK = "http://localhost:3001/callback"
APP_SECRET = os.getenv("APP_SECRET")

if not all([DOMAIN, CLIENT_ID, CLIENT_SECRET, AUDIENCE]):
    raise RuntimeError("Missing Auth0 configuration.")

app = Flask(__name__)
app.secret_key = APP_SECRET or secrets.token_hex(32)

def token_request(data):
    return requests.post(
        f"https://{DOMAIN}/oauth/token",
        json=data,
        timeout=30
    )

@app.route("/")
def home():
    state = secrets.token_urlsafe(24)
    session["state"] = state

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": CALLBACK,
        "scope": "openid profile email offline_access",
        "audience": AUDIENCE,
        "state": state
    }

    return redirect(
        f"https://{DOMAIN}/authorize?{urlencode(params)}"
    )

@app.route("/callback")
def callback():
    if request.args.get("error"):
        return (
            f"Auth0 error: {request.args.get('error')} - "
            f"{request.args.get('error_description', '')}"
        ), 400

    if request.args.get("state") != session.get("state"):
        return "Invalid OAuth state", 400

    response = token_request({
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": request.args.get("code"),
        "redirect_uri": CALLBACK
    })

    if response.status_code != 200:
        print("Authorization code exchange failed:", response.status_code)
        return "Token exchange failed. Check PowerShell.", 400

    initial = response.json()
    old_token = initial.get("refresh_token")

    print("\n" + "=" * 55)
    print("SECURENOVA - AUTH0 REFRESH TOKEN ROTATION TEST")
    print("=" * 55)
    print("AUTH0 LOGIN: SUCCESS")
    print("Initial refresh token received:", bool(old_token))

    if not old_token:
        print("RESULT: FAILED - No refresh token issued")
        return "No refresh token received.", 400

    # First use: rotate the refresh token
    rotated = token_request({
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": old_token
    })

    print("\n1. REFRESH TOKEN ROTATION")
    print("HTTP status:", rotated.status_code)

    if rotated.status_code != 200:
        print("Rotation response:", rotated.text[:500])
        print("RESULT: FAILED - Rotation did not succeed")
        return "Rotation failed. Check PowerShell.", 400

    new_data = rotated.json()
    new_token = new_data.get("refresh_token")

    print("New refresh token issued:", bool(new_token))

    if not new_token:
        print("RESULT: INCONCLUSIVE - No replacement refresh token")
        return "No replacement refresh token received.", 400

    # Second use: replay the old refresh token
    replay = token_request({
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": old_token
    })

    replay_data = replay.json()
    error = replay_data.get("error", "none")
    description = replay_data.get("error_description", "")

    print("\n2. OLD REFRESH TOKEN REPLAY")
    print("HTTP status:", replay.status_code)
    print("Auth0 error:", error)
    print("Description:", description[:300])

    rejected = replay.status_code != 200 and error == "invalid_grant"

    print("\n3. VERIFICATION")
    print("Old refresh token rejected:", rejected)
    print("FINAL RESULT:", "PASSED" if rejected else "FAILED / INCONCLUSIVE")
    print("=" * 55)

    return (
        "<h2>SecureNova Auth0 rotation test completed</h2>"
        "<p>Return to PowerShell to inspect the test results.</p>"
    )

if __name__ == "__main__":
    threading.Timer(
        1.5, lambda: webbrowser.open("http://localhost:3001")
    ).start()

    print("SecureNova Auth0 test server: http://localhost:3001")
    app.run(host="127.0.0.1", port=3001, debug=False)
