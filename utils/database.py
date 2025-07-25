# utils/database.py

import json

DB_PATH = "mock_db.py"

def get_all_users():
    try:
        from mock_db import USERS
        return USERS
    except Exception as e:
        return {}

def get_message_history(user_number):
    try:
        from mock_db import MESSAGES
        return MESSAGES.get(user_number, [])
    except Exception as e:
        return []
