from obs_logging import *
import os
import time
import json
import requests

CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost:8080/"
SCOPE = "socket.token"

TOKEN_FILE = os.path.join(os.path.dirname(__file__), "..", "streamlabs_token.json")

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


TOKEN_URL = "https://streamlabs.com/api/v2.0/token"


def request_token(auth_code):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }

    response = requests.post(TOKEN_URL, data=data)

    if response.status_code == 200:
        new_token = response.json()
        new_token["obtained_at"] = time.time()
        save_token(new_token)
        log_info("Access token received!")
        return new_token
    else:
        log_error(f'Token request failed: "{response.text}"')
        return None


def refresh_token():
    global token_data
    log_info("Refreshing access token...")

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": token_data.get("refresh_token"),
    }

    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        new_token = response.json()
        new_token["obtained_at"] = time.time()
        save_token(new_token)
        log_info("Access token refreshed!")
        return new_token
    else:
        log_error(f'Token refresh failed: "{response.text}"')
        return None


SOCKET_TOKEN_URL = "https://streamlabs.com/api/v2.0/socket/token"


def request_socket_token():
    global token_data
    log_info("Requesting socket token...")

    if not is_token_valid():
        if not refresh_token():
            log_error("No valid access token available.")
            return

    headers = {
        "accept": "application/json",
        "Authorization": f'Bearer {token_data.get("access_token")}',
    }

    response = requests.get(SOCKET_TOKEN_URL, headers=headers)

    if response.status_code == 200:
        socket_token = response.json()
        return socket_token["socket_token"]
    else:
        log_error(f"Socket token request failed: {response.text}")
        return None
