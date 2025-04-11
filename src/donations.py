from obs_logging import *

queue = []


def handle_donation_1_usd(props, prop):
    queue.append(1)
    log_info(f"Donation queue: {queue}")


def handle_donation_5_usd(props, prop):
    queue.append(5)
    log_info(f"Donation queue: {queue}")


def handle_donation_10_usd(props, prop):
    queue.append(10)
    log_info(f"Donation queue: {queue}")
