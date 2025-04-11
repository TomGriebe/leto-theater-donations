from obs_logging import *
import animations

queue = []


def handle_donation_1_usd(_, __):
    queue.append(1)
    log_info("$1 Donation!")
    log_info(f"Updated queue: {queue}")
    animations.set_idle_looping(False)


def handle_donation_5_usd(_, __):
    queue.append(5)
    log_info("$5 Donation!")
    log_info(f"Updated queue: {queue}")
    animations.set_idle_looping(False)


def handle_donation_10_usd(_, __):
    queue.append(10)
    log_info("$10 Donation!")
    log_info(f"Updated queue: {queue}")
    animations.set_idle_looping(False)
