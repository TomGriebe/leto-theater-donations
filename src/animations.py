import obspython as obs  # type: ignore
from obs_logging import *
import sources
import donations


def add_anim_ended_handler(source):
    handler = obs.obs_source_get_signal_handler(source)
    obs.signal_handler_connect(handler, "media_ended", load_next_animation)


def load_next_animation(_):
    log_info("Selecting next animation:")
    log_info(f"Donation queue: {donations.queue}")

    if len(donations.queue) > 0:
        next_donation = donations.queue.pop(0)
        source = sources.get_source_for_donation(next_donation)

        if source:
            start_media_source(source)
            obs.obs_source_release(source)
        else:
            # No source found for animation
            restart_idle()
    else:
        # Play idle animation again (if no more donations are queued)
        log_info("No donations, looping idle animation.")
        restart_idle()
        set_idle_looping(True)


def restart_idle():
    source = sources.get_idle_source()

    if source:
        obs.obs_source_media_restart(source)
        obs.obs_source_release(source)


def set_idle_looping(value):
    source = sources.get_idle_source()

    if source:
        set_looping(source, value)
        obs.obs_source_release(source)


def set_looping(source, value):
    settings = obs.obs_source_get_settings(source)
    obs.obs_data_set_bool(settings, "looping", value)
    obs.obs_source_update(source, settings)


def set_clear_on_media_end(source, value):
    settings = obs.obs_source_get_settings(source)
    obs.obs_data_set_bool(settings, "clear_on_media_end", value)
    obs.obs_source_update(source, settings)


def set_restart_on_activate(source, value):
    settings = obs.obs_source_get_settings(source)
    obs.obs_data_set_bool(settings, "restart_on_activate", value)
    obs.obs_source_update(source, settings)


def start_media_source(source):
    obs.obs_source_media_restart(source)
    set_looping(source, False)
