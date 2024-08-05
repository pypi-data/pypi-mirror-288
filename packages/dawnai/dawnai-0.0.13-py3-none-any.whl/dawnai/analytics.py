import time
import threading
from typing import Union, List, Dict, Optional

import requests

from datetime import datetime, timezone

write_key = None
api_url = "https://api.dawnai.com/"
max_queue_size = 10000
upload_size = 100
upload_interval = 0.5
buffer = []
flush_lock = threading.Lock()
debug_logs = False
flush_thread = None


def start_flush_thread():
    if debug_logs:
        print("[dawn] Open flush thread")

    global flush_thread
    if flush_thread is None:
        flush_thread = threading.Thread(target=flush_loop)
        flush_thread.daemon = True
        flush_thread.start()


def flush_loop():
    while True:
        flush()
        time.sleep(upload_interval)


def flush() -> None:
    global buffer

    if buffer is None:
        print("[dawn] ERROR -- no buffer")
        return

    if debug_logs:
        print("[dawn] Start flush")
        print("[dawn] Getting flush buffer lock")

    with flush_lock:
        current_buffer = buffer
        buffer = []

    if debug_logs:
        print("[dawn] Got flush buffer lock: buffer size", len(current_buffer))

    grouped_events = {}
    for event in current_buffer:
        endpoint = event["type"]
        data = event["data"]
        if endpoint not in grouped_events:
            grouped_events[endpoint] = []
        grouped_events[endpoint].append(data)

    for endpoint, events_data in grouped_events.items():
        if debug_logs:
            print(f"[dawn] Sending {len(events_data)} events to {endpoint}")
        send_request(endpoint, events_data)

    if debug_logs:
        print("[dawn] Flush complete")


def save_to_buffer(event: Dict[str, Union[str, Dict]]) -> None:
    global buffer

    if len(buffer) >= max_queue_size:
        print("[dawn] Buffer is full. Discarding event.")
        return

    if debug_logs:
        print(f"[dawn] Start add to buffer: {event}")

    with flush_lock:
        buffer.append(event)

    if debug_logs:
        print(f"[dawn] Added to buffer: {event}")

    start_flush_thread()


def identify(user_id: str, traits: Dict[str, Union[str, int, bool, float]]) -> None:
    data = {"user_id": user_id, "traits": traits}
    save_to_buffer({"type": "identify", "data": data})


def track(
    user_id: str,
    event: str,
    properties: Optional[Dict[str, Union[str, int, bool, float]]] = None,
    timestamp: Optional[str] = None,
) -> None:
    if timestamp is None:
        timestamp = datetime.now(timezone.utc).isoformat()
    data = {
        "user_id": user_id,
        "event": event,
        "properties": properties,
        "timestamp": timestamp,
    }
    save_to_buffer({"type": "track", "data": data})


def track_ai(
    user_id: str,
    event: str,
    model: Optional[str] = None,
    user_input: Optional[str] = None,
    output: Optional[str] = None,
    convo_id: Optional[str] = None,
    properties: Optional[Dict[str, Union[str, int, bool, float]]] = None,
    timestamp: Optional[str] = None,
) -> None:
    if not user_input and not output:
        raise ValueError("One of user_input or output must be provided and not empty.")

    if timestamp is None:
        timestamp = datetime.now(timezone.utc).isoformat()

    data = {
        "user_id": user_id,
        "event": event,
        "properties": properties or {},
        "timestamp": timestamp,
        "ai_data": {
            "model": model,
            "input": user_input,
            "output": output,
            "convo_id": convo_id,
        },
    }

    save_to_buffer({"type": "track-ai", "data": data})


def send_request(
    endpoint: str, data_entries: List[Dict[str, Union[str, Dict]]]
) -> None:
    if write_key is None:
        raise ValueError("write_key is not set")

    url = f"{api_url}{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {write_key}",
    }

    try:
        response = requests.post(url, json=data_entries, headers=headers)
        response.raise_for_status()
        if debug_logs:
            print(f"[dawn] Response: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {response.text}")
        raise
