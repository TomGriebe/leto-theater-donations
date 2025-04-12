from obs_logging import *
import obs_logging
import obspython as obs

import importlib

import animations
import donations
import obs_logging
import sources

import sl_donations
import sl_oauth
import sl_token

# Force reload of modules (OBS doesn't do it sometimes)
importlib.reload(obs_logging)
importlib.reload(animations)
importlib.reload(donations)
importlib.reload(obs_logging)
importlib.reload(sources)

importlib.reload(sl_donations)
importlib.reload(sl_oauth)
importlib.reload(sl_token)


def try_sources_setup():
    log_info("Trying to set up sources...")
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

    obs.timer_remove(try_sources_setup)
    log_info("Finished initial setup!")


# This is run as soon as the script is loaded, to set up the basic event handling.
def script_load(settings):
    log_info("Loading Leto's Theater Reactions...")

    sl_token.load_token()
    update_text_props(settings)
    obs.timer_add(try_sources_setup, 500)

    if sl_token.token_data:
        if not sl_token.is_token_valid():
            log_info("Token is outdated, refreshing...")
            sl_token.refresh_token()
        else:
            log_info("Token is still valid.")
    else:
        log_warn("No token loaded, you need to press the OAuth button!")


def update_text_props(settings):
    sl_token.CLIENT_ID = obs.obs_data_get_string(settings, "streamlabs_client_id")
    sl_token.CLIENT_SECRET = obs.obs_data_get_string(settings, "streamlabs_client_secret")

    try:
        donate_value = obs.obs_data_get_string(settings, "donate_value")
        donations.amount = float(donate_value)
    except:
        donations.amount = None


def script_update(settings):
    update_text_props(settings)


# This function sets up the UI properties (like buttons) for the script.
def script_properties():
    props = obs.obs_properties_create()

    # Mock donations
    obs.obs_properties_add_text(props, "donate_title", "Mock donations:", obs.OBS_TEXT_INFO)
    obs.obs_properties_add_text(props, "donate_value", "Donation:", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_button(props, "donate_btn", "Donate!", donations.handle_donation)

    obs.obs_properties_add_text(props, "separator1", "", obs.OBS_TEXT_INFO)

    # Streamlabs setup
    obs.obs_properties_add_text(props, "streamlabs_title", "Streamlabs setup:", obs.OBS_TEXT_INFO)
    obs.obs_properties_add_text(props, "streamlabs_client_id", "Client ID:", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "streamlabs_client_secret", "Client Secret:", obs.OBS_TEXT_PASSWORD)
    obs.obs_properties_add_button(props, "streamlabs_auth", "Authenticate", sl_oauth.initiate_oauth_flow)

    return props


# This provides a simple description for the script in the OBS UI.
def script_description():
    return "A script to loop an idle animation and react to Streamlabs tips."
