from obs_logging import *
import asyncio
import threading
import sl_token
import socketio
import animations
import sl_token

event_loop = None
loop_thread = None
loop_ready = threading.Event()
disconnected = threading.Event()

sio = None


async def connect_websocket():
    global sio

    ws_token = sl_token.request_socket_token()

    if not ws_token:
        log_error("No socket token could be acquired.")
        return

    try:
        sio = socketio.AsyncClient()

        @sio.on("event")
        def handle_event(data):
            if data["type"] == "donation":
                event_donations = data["message"]
                log_info(f"{len(event_donations)} donations!")

                for donation in event_donations:
                    if donation["currency"] != "USD":
                        continue

                    try:
                        amount = float(donation["amount"])
                        add_donation(amount)
                    except:
                        log_warn(f"Could not convert '{donation['amount']} to float.'")
            else:
                log_info("non-donation event: " + str(data))

        await sio.connect(f"https://sockets.streamlabs.com?token={ws_token}")

        asyncio.create_task(sio.wait())
    except Exception as e:
        log_error(f"Failed to connect: {e}")


async def disconnect_websocket():
    global sio

    if sio:
        await sio.disconnect()
        disconnected.set()


def start_event_loop():
    global event_loop, loop_ready
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    loop_ready.set()
    event_loop.run_forever()


def activate():
    global event_loop, loop_thread

    if not sl_token.token_data or not sl_token.is_token_valid():
        log_warn("Cannot start websockets without valid token.")
        return

    if not event_loop or not event_loop.is_running():
        log_info("Starting websocket event loop.")
        loop_ready.clear()
        loop_thread = threading.Thread(target=start_event_loop, daemon=True)
        loop_thread.start()

        if not loop_ready.wait(timeout=5):
            log_error("Event loop did not start in time!")
            return

    else:
        log_warn("Websocket event loop is already running.")

    log_info("Starting ws_connect coroutine.")
    future = asyncio.run_coroutine_threadsafe(connect_websocket(), event_loop)
    future.result()


def deactivate():
    global event_loop, loop_thread, disconnected

    if not event_loop or not event_loop.is_running() and not loop_thread or not loop_thread.is_alive():
        log_warn("No event loop or loop thread to stop.")
        return
    elif not event_loop or not event_loop.is_running():
        log_warn("No event loop to stop.")
        return
    elif not loop_thread or not loop_thread.is_alive():
        log_warn("No loop thread to stop.")
        return

    disconnected.clear()

    # Stop listening on the websocket
    log_info("Starting ws_disconnect coroutine.")
    future = asyncio.run_coroutine_threadsafe(disconnect_websocket(), event_loop)
    future.result()

    disconnected.wait(timeout=10)

    # Stop the event loop
    log_info("Waiting for event loop to stop...")
    event_loop.call_soon_threadsafe(event_loop.stop)
    loop_thread.join()
    log_info("Event loop stopped!")


queue = []


def add_donation(amount):
    queue.append(amount)
    log_info(f"${amount} Donation!")
    log_info(f"Updated queue: {queue}")
    animations.set_idle_looping(False)
