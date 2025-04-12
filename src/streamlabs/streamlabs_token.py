from obs_logging import *
import sys
import os
import time
import threading
import webbrowser
import urllib.parse
import json
import requests
import asyncio
import websockets

CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost:8080/"
SCOPE = "donations.read"
OAUTH_PORT = 8080

TOKEN_FILE = os.path.join(os.path.dirname(__file__), "streamlabs_token.json")

token_data = {}


def save_token(token):
    global token_data
    token_data = token

    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)
    log_info(f"Saved token data to file.")


def load_token():
    global token_data

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            token_data = json.load(f)

        log_info("Loaded token data from file.")
        return token_data
    else:
        return None


def is_token_valid():
    if not token_data:
        return False

    now = time.time()
    obtained_at = int(token_data.get("obtained_at", 0))
    expires_in = int(token_data.get("expires_in", 0))
    return now < obtained_at + expires_in - 60


def refresh_token():
    global token_data
    log_info("Refreshing access token...")
    refresh_url = "https://streamlabs.com/api/v2.0/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": token_data.get("refresh_token"),
    }

    response = requests.post(refresh_url, data=data)
    if response.status_code == 200:
        new_token = response.json()
        new_token["obtained_at"] = time.time()
        save_token(new_token)
        log_info("Access token refreshed!")
        return new_token
    else:
        log_error(f'Token refresh failed: "{response.text}"')
        return None
