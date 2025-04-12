from obs_logging import *

CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost:8080/"
SCOPE = "donations.read"
OAUTH_PORT = 8080


def start_oauth():
    log_info("Starting OAuth.")
