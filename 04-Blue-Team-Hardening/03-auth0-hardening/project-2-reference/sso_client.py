
import os
import secrets
import requests

from flask import Flask, redirect, request, session
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()

DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("SSO_CLIENT_ID")
CLIENT_SECRET = os.getenv("SSO_CLIENT_SECRET")
APP_SECRET = os.getenv("APP_SECRET")

CALLBACK_URL = "http://localhost:3001/callback"
AUTH_URL = f"https://{DOMAIN}/authorize"
TOKEN_URL = f"https://{DOMAIN}/oauth/token"

app = Flask(__name__)
app.secret_key = APP_SECRET


@app.route("/")
def home():
    if "user" in session:
        return f"""
        <h1>SecureNova SSO Client</h1>
        <h2>SSO Login Successful</h2>
        <p>User: {session['user']}</p>
        <p>Authenticated through Auth0.</p>
        """
    return '<a href="/login">Login with Auth0</a>'


@app.route("/login")
def login():
    state = secrets.token_urlsafe(16)
    session["state"] = state

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": CALLBACK_URL,
        "scope": "openid profile email",
        "state": state
    }

    return redirect(AUTH_URL + "?" + urlencode(params))


@app.route("/callback")
def callback():
    if request.args.get("state") != session.get("state"):
        return "Invalid state", 400

    code = request.args.get("code")

    response = requests.post(
        TOKEN_URL,
        json={
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "redirect_uri": CALLBACK_URL
        },
        timeout=20
    )

    if not response.ok:
        return f"Token exchange failed: {response.text}", 400

    token_data = response.json()

    import jwt
    from jwt import PyJWKClient

    jwks = PyJWKClient(
        f"https://{DOMAIN}/.well-known/jwks.json"
    )
    signing_key = jwks.get_signing_key_from_jwt(
        token_data["id_token"]
    )

    claims = jwt.decode(
        token_data["id_token"],
        signing_key.key,
        algorithms=["RS256"],
        audience=CLIENT_ID,
        issuer=f"https://{DOMAIN}/"
    )

    session["user"] = claims.get("email", claims["sub"])

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    if not all([DOMAIN, CLIENT_ID, CLIENT_SECRET, APP_SECRET]):
        raise RuntimeError("Check the SSO environment variables in .env")

    print("SecureNova SSO Client running at http://localhost:3001")
    app.run(host="127.0.0.1", port=3001, debug=False)
