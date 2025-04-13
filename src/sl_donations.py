from obs_logging import *
import asyncio
import threading
import websockets
import sl_token

event_loop = None
loop_thread = None
loop_ready = threading.Event()

websocket_connection = None
active = False


async def connect_websocket():
    global websocket_connection, active

    if not sl_token.is_token_valid():
        if not sl_token.refresh_token():
            log_error("No valid access token available.")
            return

    ws_token = sl_token.token_data.get("access_token")
    ws_url = f"wss://sockets.streamlabs.com/socket.io/?token={ws_token}&EIO=3&transport=websocket"
    log_info(ws_url)

    try:
        websocket_connection = await websockets.connect(ws_url)
        active = True
        log_info("Connected to Streamlabs websocket.")

        asyncio.create_task(listen_websocket())
    except Exception as e:
        log_error(f"Failed to connect: {e}")


async def disconnect_websocket():
    global websocket_connection, active
    active = False

    if websocket_connection:
        await websocket_connection.close()
        log_info("Websocket connection closed.")


async def listen_websocket():
    global websocket_connection, active

    try:
        while active:
            message = await websocket_connection.recv()
            log_info(f"Received message: {message}")
    except websockets.ConnectionClosed:
        log_info("Websocket connection was closed.")
    except Exception as e:
        log_error(f"Error while receiving message: {e}")


def start_event_loop():
    global event_loop, loop_ready
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    loop_ready.set()
    event_loop.run_forever()


def activate(_, __):
    global event_loop, loop_thread

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


def deactivate(_, __):
    global event_loop, loop_thread

    if not event_loop or not event_loop.is_running() and not loop_thread or not loop_thread.is_alive():
        log_warn("No event loop or loop thread to stop.")
        return
    elif not event_loop or not event_loop.is_running():
        log_warn("No event loop to stop.")
        return
    elif not loop_thread or not loop_thread.is_alive():
        log_warn("No loop thread to stop.")
        return

    # Stop listening on the websocket
    log_info("Starting ws_disconnect coroutine.")
    future = asyncio.run_coroutine_threadsafe(disconnect_websocket(), event_loop)
    future.result()

    # Stop the event loop
    log_info("Waiting for event loop to stop...")
    event_loop.call_soon_threadsafe(event_loop.stop)
    loop_thread.join()
    log_info("Event loop stopped!")
