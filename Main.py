from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from Responses import process_cooked, get_response

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content.lower()
    channel: str = str(message.channel)

    if "cooked" in user_message:
        should_respond, count = process_cooked(username)
        if should_respond:
            response: str = get_response(count)
            await message.channel.send(response)

def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()