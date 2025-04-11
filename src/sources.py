import obspython as obs  # type: ignore
from obs_logging import *

IDLE_SOURCE = "Theater Idle"

TIP_1_USD_SOURCE = "Theater Tip 1 USD"
TIP_5_USD_SOURCE = "Theater Tip 5 USD"
TIP_10_USD_SOURCE = "Theater Tip 10 USD"


def get_idle_source():
    source = obs.obs_get_source_by_name(IDLE_SOURCE)

    if source is None:
        obs.script_log(obs.LOG_WARNING, "Idle media source not found")
    return source


def get_media_source_name_for_donation(amount):
    if amount is None:
        log_info("more logs")
        log_info("amount is None")
        return ""

    log_info(f"amount is {amount}")

    source_name = ""

    if amount >= 1:
        source_name = TIP_1_USD_SOURCE
    if amount >= 5:
        source_name = TIP_5_USD_SOURCE
    if amount >= 10:
        source_name = TIP_10_USD_SOURCE

    if source_name:
        log_info(f"Chosen animation: '{source_name}'")
        return source_name
    else:
        log_warn(f"Could not find fitting animation for ${amount} tip")
        return ""
