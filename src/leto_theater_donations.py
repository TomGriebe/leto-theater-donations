import obspython as obs  # type: ignore
from obs_logging import *

import importlib
import animations
import donations
import obs_logging
import sources

importlib.reload(animations)
importlib.reload(donations)
importlib.reload(obs_logging)
importlib.reload(sources)


# This is run as soon as the script is loaded, to set up the basic event handling.
def script_load(settings):
    log_info("Loading script...")
    animations.add_loop_ended_handler()


def script_unload():
    log_info("Unloading script...")
    animations.remove_loop_ended_handler()


# This function sets up the UI properties (like buttons) for the script.
def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_button(props, "donate_1_btn", "Donate $1!", donations.handle_donation_1_usd)
    obs.obs_properties_add_button(props, "donate_5_btn", "Donate $5!", donations.handle_donation_5_usd)
    obs.obs_properties_add_button(props, "donate_10_btn", "Donate $10!", donations.handle_donation_10_usd)
    return props


# This provides a simple description for the script in the OBS UI.
def script_description():
    return "A script to loop an idle animation and react to Streamlabs tips."
