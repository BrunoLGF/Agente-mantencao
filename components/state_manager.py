# components/state_manager.py

import json
from datetime import datetime

def get_current_timestamp():
    return datetime.now().strftime("%H:%M")

def load_state():
    try:
        with open("data/state.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "os_counter": 1,
            "open_os": {},
            "history": {},
            "active_user": None,
            "notifications": {}
        }

def save_state(state):
    with open("data/state.json", "w") as f:
        json.dump(state, f, indent=4)

def append_history(state, phone_number, sender, message):
    if phone_number not in state["history"]:
        state["history"][phone_number] = []
    state["history"][phone_number].append({
        "timestamp": get_current_timestamp(),
        "sender": sender,
        "message": message
    })

def notify_user(state, phone_number):
    if phone_number not in state["notifications"]:
        state["notifications"][phone_number] = 0
    state["notifications"][phone_number] += 1

def clear_notifications(state, phone_number):
    state["notifications"][phone_number] = 0
