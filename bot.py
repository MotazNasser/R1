import nest_asyncio
from telethon import TelegramClient, events
import uuid
import os
import asyncio

# Allow nested event loops
nest_asyncio.apply()

# Retrieve values from environment variables
api_id = int(os.environ['API_ID'])  # Your actual API ID (as an integer)
api_hash = os.environ['API_HASH']  # Your actual API Hash (keep it as a string)
bot_token = os.environ['BOT_TOKEN']  # Your actual Bot Token (keep it as a string)

async def main():
    session_name = str(uuid.uuid4())
    client = TelegramClient(session_name, api_id, api_hash)

    await client.start(bot_token=bot_token)

    print("Bot is running and listening for forwarded messages...")  # Debug message

    @client.on(events.NewMessage())
    async def handler(event):
        message_text = event.message.message
        print(f"Received forwarded message: {message_text}")  # Print received message

        parse_trading_signal(message_text)

    await client.run_until_disconnected()

def parse_trading_signal(message):
    print(f"Parsing signal: {message}")

if __name__ == "__main__":
    asyncio.run(main())
