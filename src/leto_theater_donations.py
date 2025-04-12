import obspython as obs  # type: ignore
from obs_logging import *

import importlib
import animations
import donations
import obs_logging
import sources
import streamlabs

importlib.reload(animations)
importlib.reload(donations)
importlib.reload(obs_logging)
importlib.reload(sources)
importlib.reload(streamlabs)


def try_setup():
    log_info("Trying to set up sources")
    idle_source = sources.get_idle_source()

    if idle_source:
        animations.set_looping(idle_source, True)
        animations.set_clear_on_media_end(idle_source, True)
        animations.set_restart_on_activate(idle_source, True)
        animations.add_anim_ended_handler(idle_source)
        obs.obs_source_release(idle_source)
    else:
        log_warn("Idle source could not be found.")
        return

    donation_sources = sources.get_all_donation_sources()

    for source in donation_sources:
        if source:
            animations.set_looping(source, False)
            animations.set_clear_on_media_end(source, True)
            animations.set_restart_on_activate(source, False)
            animations.add_anim_ended_handler(source)
            obs.obs_source_media_stop(source)
            obs.obs_source_release(source)
        else:
            log_warn("One of the donation sources could not be found.")
            return

    obs.timer_remove(try_setup)
    log_info("Finished initial setup!")


# This is run as soon as the script is loaded, to set up the basic event handling.
def script_load(_):
    log_info("Loading script")
    obs.timer_add(try_setup, 500)


def script_update(settings):
    streamlabs.api_key = obs.obs_data_get_string(settings, "streamlabs_api_key")


# This function sets up the UI properties (like buttons) for the script.
def script_properties():
    props = obs.obs_properties_create()

    # Streamlabs API Key
    obs.obs_properties_add_text(props, "streamlabs_api_key", "Streamlabs API Key", obs.OBS_TEXT_PASSWORD)

    # Mock donation buttons
    obs.obs_properties_add_button(props, "donate_1_btn", "Donate $1!", donations.handle_donation_1_usd)
    obs.obs_properties_add_button(props, "donate_5_btn", "Donate $5!", donations.handle_donation_5_usd)
    obs.obs_properties_add_button(props, "donate_10_btn", "Donate $10!", donations.handle_donation_10_usd)

    return props


# This provides a simple description for the script in the OBS UI.
def script_description():
    return "A script to loop an idle animation and react to Streamlabs tips."
