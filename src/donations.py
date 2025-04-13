from obs_logging import *
import sl_donations
import animations

amount = 0
queue = []


def handle_donation(_, __):
    sl_donations.post_donation(amount)


def add_donation(amount):
    queue.append(amount)
    log_info(f"${amount} Donation!")
    log_info(f"Updated queue: {queue}")
    animations.set_idle_looping(False)
