import json
from datetime import datetime, timedelta
from typing import Optional, List, Tuple

DATA_FILE = 'cooked_data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        return (
            data['cooked_count'],
            {k: datetime.fromisoformat(v) for k, v in data['last_response_date'].items()},
            data.get('total_cooked_count', 0)
        )
    except (FileNotFoundError, json.JSONDecodeError):
        return {}, {}, 0

def save_data():
    data = {
        'cooked_count': cooked_count,
        'last_response_date': {k: v.isoformat() for k, v in last_response_date.items()},
        'total_cooked_count': total_cooked_count
    }
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

cooked_count, last_response_date, total_cooked_count = load_data()

def process_cooked(username: str) -> tuple[bool, int, int]:
    global total_cooked_count
    today = datetime.now().date()

    if username not in cooked_count:
        cooked_count[username] = 0

    cooked_count[username] += 1
    total_cooked_count += 1

    should_respond = False
    if username not in last_response_date or last_response_date[username].date() < today:
        should_respond = True
        last_response_date[username] = datetime.now()

    save_data()  # Save data after each update
    return should_respond, cooked_count[username], total_cooked_count

def get_response(count: int) -> str:
    if count == 1:
        return f"stop with the doom posting"
    elif count < 10:
        return f"kys"
    elif count < 25:
        return f"Wow, {count} times cooked"
    elif count < 35:
        return f"Your parents don't love you"
    elif count < 50:
        return f"1984"
    elif count < 75:
        return f"Bro thinks he's Jeremy Wu"
    else:
        return f"Are you mentally ill?"


def get_cooked_count(username: str) -> int:
    return cooked_count.get(username, 0)


def get_total_cooked_count() -> int:
    return total_cooked_count


def format_cooked_count_message(username: str, count: int) -> str:
    if count == 0:
        return f"{username} hasn't been cooked yet."
    elif count == 1:
        return f"{username} has been cooked once."
    else:
        return f"{username} has been cooked {count} times."


def get_leaderboard(top_n: int = 10) -> List[Tuple[str, int]]:
    sorted_counts = sorted(cooked_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_counts[:top_n]


def format_leaderboard(leaderboard: List[Tuple[str, int]]) -> str:
    if not leaderboard:
        return "No one has been cooked yet!"

    formatted = "🏆 Cooked Leaderboard 🏆\n\n"
    current_rank = 1
    previous_count = None

    for i, (username, count) in enumerate(leaderboard, 1):
        if count != previous_count:
            current_rank = i
        formatted += f"{current_rank}. {username}: {count} times\n"
        previous_count = count

    return formatted