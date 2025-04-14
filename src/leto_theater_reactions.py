from obs_logging import *
import obs_logging
import obspython as obs

import importlib

import animations
import test_donations
import obs_logging
import sources

import sl_donations
import sl_oauth
import sl_token

# Force reload of modules (OBS doesn't do it sometimes)
importlib.reload(obs_logging)
importlib.reload(animations)
importlib.reload(test_donations)
importlib.reload(obs_logging)
importlib.reload(sources)

importlib.reload(sl_donations)
importlib.reload(sl_oauth)
importlib.reload(sl_token)

failed_sources_once = False


def try_sources_setup():
    global failed_sources_once
    log_info("Trying to set up sources...")
    idle_source = sources.get_idle_source()

    if idle_source:
        animations.set_looping(idle_source, True)
        animations.set_clear_on_media_end(idle_source, True)
        animations.set_restart_on_activate(idle_source, True)
        animations.add_anim_ended_handler(idle_source)
        obs.obs_source_release(idle_source)
    else:
        if not failed_sources_once:
            log_warn("Idle source could not be found.")
            failed_sources_once = True
        return

    donation_sources = sources.get_all_donation_sources()

    for source_name in donation_sources:
        source = obs.obs_get_source_by_name(source_name)

        if source:
            animations.set_looping(source, False)
            animations.set_clear_on_media_end(source, True)
            animations.set_restart_on_activate(source, False)
            animations.add_anim_ended_handler(source)
            obs.obs_source_media_stop(source)
            obs.obs_source_release(source)
        else:
            if not failed_sources_once:
                log_warn("One of the donation sources could not be found.")
                failed_sources_once = True
            return

    obs.timer_remove(try_sources_setup)
    log_info("Sources are set up!")


# This is run as soon as the script is loaded, to set up the basic event handling.
def script_load(settings):
    log_info("=== Leto's Theater Reactions ===")
    log_info("Initializing script...")

    get_text_field_values(settings)

    sl_token.load_token()

    if (not sl_token.token_data) or (not sl_token.is_token_valid() and not sl_token.refresh_token()):
        log_error("Failed Setup: No valid Streamlabs token.")
        log_error('Enter "Client ID" and "Client Secret", then press "OAuth".')
        log_error("Afterwards, restart the script or OBS.")
        return

    # Setup websocket thread and listen for donations
    sl_donations.activate()

    # Start sources setup with short delay
    obs.timer_add(try_sources_setup, 1000)


def script_unload():
    sl_donations.deactivate()
    log_info("Script unload finished\n")


def get_text_field_values(settings):
    sl_token.CLIENT_ID = obs.obs_data_get_string(settings, "sl_client_id")
    sl_token.CLIENT_SECRET = obs.obs_data_get_string(settings, "sl_client_secret")

    try:
        donate_value = obs.obs_data_get_string(settings, "donate_value")
        test_donations.test_donation_value = float(donate_value)
    except:
        test_donations.test_donation_value = None


def script_update(settings):
    get_text_field_values(settings)


# This function sets up the UI properties (like buttons) for the script.
def script_properties():
    props = obs.obs_properties_create()

    # Mock donations
    obs.obs_properties_add_text(props, "donate_title", "Send test donation:", obs.OBS_TEXT_INFO)
    obs.obs_properties_add_text(props, "donate_value", "Value:", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_button(props, "donate_btn", "Send", test_donations.handle_test_donation)

    obs.obs_properties_add_text(props, "separator1", "", obs.OBS_TEXT_INFO)

    # Streamlabs setup
    obs.obs_properties_add_text(props, "sl_title", "Streamlabs setup:", obs.OBS_TEXT_INFO)
    obs.obs_properties_add_text(props, "sl_client_id", "Client ID:", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "sl_client_secret", "Client Secret:", obs.OBS_TEXT_PASSWORD)
    obs.obs_properties_add_button(props, "sl_oauth_btn", "OAuth", sl_oauth.handle_oauth)

    obs.obs_properties_add_text(props, "separator2", "", obs.OBS_TEXT_INFO)

    return props


# This provides a simple description for the script in the OBS UI.
def script_description():
    return "A script to loop an idle animation and react to Streamlabs tips."
