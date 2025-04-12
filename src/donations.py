from obs_logging import *
import animations

amount = 0
queue = []


def handle_donation(_, __):
    if amount:
        queue.append(amount)
        log_info(f"${amount} Donation!")
        log_info(f"Updated queue: {queue}")
        animations.set_idle_looping(False)
