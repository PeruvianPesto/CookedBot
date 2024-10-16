from typing import Final
import os
import asyncio
from dotenv import load_dotenv
from discord import Intents, Client, Message, Activity, ActivityType
from Responses import (
    process_cooked, get_response, get_cooked_count, format_cooked_count_message,
    load_data, get_total_cooked_count, get_leaderboard, format_leaderboard
)

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

async def update_status():
    while True:
        total_count = get_total_cooked_count()
        activity = Activity(type=ActivityType.watching, name=f"{total_count} cooked")
        await client.change_presence(activity=activity)
        await asyncio.sleep(60)  # Update every 60 seconds

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    load_data()  # Load saved data when the bot starts
    client.loop.create_task(update_status())

@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content.lower()
    channel: str = str(message.channel)

    if user_message.startswith('!cooked'):
        if user_message == '!cookedlb':
            # Display leaderboard
            leaderboard = get_leaderboard()
            response = format_leaderboard(leaderboard)
        elif message.mentions:
            # Check cooked count for mentioned user
            mentioned_user = str(message.mentions[0])
            count = get_cooked_count(mentioned_user)
            response = format_cooked_count_message(mentioned_user, count)
        else:
            # Check cooked count for message author
            count = get_cooked_count(username)
            response = format_cooked_count_message(username, count)
        await message.channel.send(response)
    elif "cooked" in user_message or "wraps" in user_message:
        should_respond, count, total_count = process_cooked(username)
        if should_respond:
            response: str = get_response(count)
            await message.channel.send(response)

def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()