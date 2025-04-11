import obspython as obs  # type: ignore
from obs_logging import *
import sources
import donations

idle_signal_handler = None


def add_loop_ended_handler():
    source = sources.get_idle_source()

    if source:
        global idle_signal_handler
        idle_signal_handler = obs.obs_source_get_signal_handler(source)

        if idle_signal_handler:
            log_info("Connecting handler to 'media_ended' signal")
            obs.signal_handler_connect(idle_signal_handler, "media_ended", on_idle_loop_end)

        obs.obs_source_release(source)


def remove_loop_ended_handler():
    global idle_signal_handler

    if idle_signal_handler:
        log_info("Disconnecting handler from 'media_ended' signal")
        obs.signal_handler_disconnect(idle_signal_handler, "media_ended", on_idle_loop_end)


def on_idle_loop_end(data):
    next_donation = None
    donation_source = None

    if len(donations.queue) > 0:
        next_donation = donations.queue.pop(0)
        log_info(f"${next_donation} donation is next")
        donation_source = sources.get_source_for_donation(next_donation)

    if donation_source:
        start_media_source_solo(donation_source)
        obs.obs_source_release(donation_source)
    else:
        log_info("Restarting idle")
        restart_idle()

    log_info(f"Donation queue: {donations.queue}")


def restart_idle():
    source = sources.get_idle_source()

    if source:
        obs.obs_source_media_restart(source)
        obs.obs_source_release(source)


def start_media_source_solo(source):
    log_info(f"Starting animation in solo mode")
    # source = obs.obs_get_source_by_name(name)
    # obs.obs_source_release(source)
