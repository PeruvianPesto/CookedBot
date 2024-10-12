from datetime import datetime, timedelta
from typing import Optional

cooked_count = {}
last_response_date = {}

def process_cooked(username: str) -> tuple[bool, int]:
    today = datetime.now().date()

    if username not in cooked_count:
        cooked_count[username] = 0

    cooked_count[username] += 1

    should_respond = False
    if username not in last_response_date or last_response_date[username] < today:
        should_respond = True
        last_response_date[username] = today

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
        return f"{username} Cooked Count: 0"
    elif count == 1:
        return f"{username} Cooked Count: 1"
    else:
        return f"{username} Cooked Count: {count}"