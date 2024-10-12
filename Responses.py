from datetime import datetime, timedelta

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
        return "Stfu Chud"
    elif count < 5:
        return f"Cooked again! That's {count} times now."
    elif count < 10:
        return f"Wow, {count} times cooked! You're on a roll!"
    else:
        return f"Incredible! You've been cooked {count} times! Are you okay?"