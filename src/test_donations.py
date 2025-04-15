from obs_logging import *
import sl_token
import sl_donations
import requests

test_donation_value = 0


def handle_test_donation_offline(_, __):
    sl_donations.add_donation(test_donation_value)


def handle_test_donation(_, __):
    test_donation(test_donation_value)


def test_donation(amount):
    if not sl_token.is_token_valid():
        if not sl_token.refresh_token():
            log_error("Cannot post donation: no valid tokens.")
            return

    access_token = sl_token.token_data.get("access_token")
    url = "https://streamlabs.com/api/v2.0/donations"

    payload = {
        "name": "LetoDoesTests",
        "message": "This is a test donation :3",
        "identifier": "test-donation",
        "amount": amount,
        "currency": "USD",
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        log_info("Test donation sent!")
    else:
        log_error(f"Could not send test donation: {response.reason}")
