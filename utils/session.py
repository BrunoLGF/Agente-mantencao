import json
from typing import Dict

DATA_PATH = "data/state.json"

def load_state() -> Dict:
    try:
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_state(state: Dict):
    with open(DATA_PATH, "w") as f:
        json.dump(state, f, indent=4)

def get_users() -> list:
    state = load_state()
    return list(state.get("conversations", {}).keys())

def get_current_user() -> str:
    state = load_state()
    return state.get("current_user", "")

def switch_user(user_id: str):
    state = load_state()
    state["current_user"] = user_id
    save_state(state)

def unread_counts() -> Dict[str, int]:
    state = load_state()
    counts = {}
    for user, msgs in state.get("conversations", {}).items():
        unread = [m for m in msgs if m.get("role") == "user" and not m.get("read", False)]
        counts[user] = len(unread)
    return counts
