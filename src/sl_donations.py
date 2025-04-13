from obs_logging import *
import sl_token
import websockets
import asyncio
import threading

websocket = None
stop_event = threading.Event()


async def listen_streamlabs():
    if not sl_token.is_token_valid():
        if not sl_token.refresh_token():
            log_error("No valid access token available.")
            return

    ws_token = sl_token.token_data.get("access_token")
    ws_url = f"wss://sockets.streamlabs.com/socket.io/?token={ws_token}&EIO=3&transport=websocket"

    log_info("Connecting to Streamlabs websocket...")
    log_info(ws_url)

    try:
        async with websockets.connect(ws_url) as ws:
            global websocket
            websocket = ws
            log_info("Connected to Streamlabs websocket!")

            while True:
                message = await ws.recv()
                log_info(f"Received message: {message}")
                # todo: queue donation

            log_info("Stop event was set, stopping websocket listening.")

    except Exception as e:
        log_error(f"Websocket error: {e}")


def start_streamlabs_listener():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(listen_streamlabs())


def stop_listener_thread(_, __):
    global websocket
    global stop_event

    log_info("Setting stop event.")
    stop_event.set()

    if websocket:
        log_info("Closing websocket.")
        websocket.close()


def start_listener_thread(_, __):
    global stop_event

    stop_event.clear()
    thread = threading.Thread(target=start_streamlabs_listener, daemon=True)
    thread.start()
