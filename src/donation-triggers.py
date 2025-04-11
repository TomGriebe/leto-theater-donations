import obspython as obs  # type: ignore

IDLE_SOURCE = "Theater Idle"
donations = 0


def get_idle_source():
    source = obs.obs_get_source_by_name(IDLE_SOURCE)

    if source is None:
        obs.script_log(obs.LOG_WARNING, "Idle media source not found")
    return source


def on_idle_loop_end(data):
    source = get_idle_source()

    if source is None:
        return

    if donations > 0:
        print("Should play donation media now")
    else:
        log_info("No donations, continuing idle")
        obs.obs_source_media_restart(source)
        obs.obs_source_release(source)


def setup_idle_loop():
    source = get_idle_source()

    if source:
        handler = obs.obs_source_get_signal_handler(source)
        obs.signal_handler_connect(handler, "media_ended", on_idle_loop_end)
        obs.obs_source_release(source)


def log_info(message):
    obs.script_log(obs.LOG_INFO, message)


def handle_donation(props, prop):
    global donations
    donations += 1
    log_info(f"Donation queue: {donations}")


# This is run as soon as the script is loaded, to set up the basic event handling.
def script_load(settings):
    log_info("Loading script")
    setup_idle_loop()


# This function sets up the UI properties (like buttons) for the script.
def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_button(props, "dono_button", "Donate!", handle_donation)
    return props


# This provides a simple description for the script in the OBS UI.
def script_description():
    return "A simple script to add a button to OBS that triggers custom functionality when pressed."
