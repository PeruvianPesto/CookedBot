import json
from datetime import datetime, timedelta
from typing import Optional

DATA_FILE = 'cooked_data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        return data['cooked_count'], {k: datetime.fromisoformat(v) for k, v in data['last_response_date'].items()}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}, {}

def save_data():
    data = {
        'cooked_count': cooked_count,
        'last_response_date': {k: v.isoformat() for k, v in last_response_date.items()}
    }
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

cooked_count, last_response_date = load_data()

def process_cooked(username: str) -> tuple[bool, int]:
    today = datetime.now().date()

    if username not in cooked_count:
        cooked_count[username] = 0

    cooked_count[username] += 1

    should_respond = False
    if username not in last_response_date or last_response_date[username].date() < today:
        should_respond = True
        last_response_date[username] = datetime.now()

    save_data()  # Save data after each update
    return should_respond, cooked_count[username]

def get_response(count: int) -> str:
    if count == 1:
        return f"stop with the doom posting"
    elif count < 5:
        return f"That's the {count} doom post"
    elif count < 10:
        return f"Wow, {count} times cooked"
    else:
        return f"Are you mentally ill?"

def get_cooked_count(username: str) -> int:
    return cooked_count.get(username, 0)

def format_cooked_count_message(username: str, count: int) -> str:
    if count == 0:
        return f"{username} hasn't been cooked yet."
    elif count == 1:
        return f"{username} has been cooked once."
    else:
        return f"{username} has been cooked {count} times."