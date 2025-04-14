import obspython as obs  # type: ignore
from obs_logging import *
import random

MAX_DONATION = 1000000
IDLE_SOURCE = "Theater Idle"


sources = [
    {"name": "Theater Tip 1 USD", "from": 0, "to": 5},
    {"name": "Theater Tip 5 USD", "from": 5, "to": 10},
    {"name": "Theater Tip 10 USD", "from": 10, "to": MAX_DONATION},
]


def get_source_name_for_amount(sources, amount):
    matching = [source for source in sources if source["from"] <= amount < source["to"]]

    if not matching:
        return None

    return random.choice(matching)["name"]


def get_idle_source():
    return obs.obs_get_source_by_name(IDLE_SOURCE)


def get_source_for_donation(amount):
    if amount is None:
        return None

    source_name = get_source_name_for_amount(amount)

    if source_name:
        log_info(f"Chosen animation: '{source_name}'.")
        source = obs.obs_get_source_by_name(source_name)

        if source:
            return source
        else:
            log_warn(f"Could not find source for name '{source_name}'.")
    else:
        log_warn(f"Could not find fitting animation for ${amount} tip.")


def get_all_donation_sources():
    return [source["name"] for source in sources]
