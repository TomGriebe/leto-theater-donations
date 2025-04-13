import obspython as obs  # type: ignore
from obs_logging import *

IDLE_SOURCE = "Theater Idle"

TIP_1_USD_SOURCE = "Theater Tip 1 USD"
TIP_5_USD_SOURCE = "Theater Tip 5 USD"
TIP_10_USD_SOURCE = "Theater Tip 10 USD"


def get_idle_source():
    return obs.obs_get_source_by_name(IDLE_SOURCE)


def get_source_for_donation(amount):
    if amount is None:
        return None

    source_name = None

    if amount >= 1:
        source_name = TIP_1_USD_SOURCE
    if amount >= 5:
        source_name = TIP_5_USD_SOURCE
    if amount >= 10:
        source_name = TIP_10_USD_SOURCE

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
    return [
        obs.obs_get_source_by_name(TIP_1_USD_SOURCE),
        obs.obs_get_source_by_name(TIP_5_USD_SOURCE),
        obs.obs_get_source_by_name(TIP_10_USD_SOURCE),
    ]
