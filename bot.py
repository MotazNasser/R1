import nest_asyncio
from telethon import TelegramClient, events
import uuid
import os
import asyncio
import re
from binance.client import Client

# Allow nested event loops
nest_asyncio.apply()

# Retrieve values from environment variables
api_id = int(os.environ['API_ID'])  # Your actual API ID (as an integer)
api_hash = os.environ['API_HASH']  # Your actual API Hash (keep it as a string)
bot_token = os.environ['BOT_TOKEN']  # Your actual Bot Token (keep it as a string)

# Initialize the Binance client
binance_api_key = os.environ['BINANCE_API_KEY']  # Your actual Binance API Key
binance_api_secret = os.environ['BINANCE_API_SECRET']  # Your actual Binance API Secret
binance_client = Client(binance_api_key, binance_api_secret)

async def main():
    session_name = str(uuid.uuid4())
    client = TelegramClient(session_name, api_id, api_hash)

    await client.start(bot_token=bot_token)

    print("Bot is running and listening for forwarded messages...")  # Debug message

    @client.on(events.NewMessage())
    async def handler(event):
        message_text = event.message.message
        print(f"Received message: {message_text}")  # Print received message

   
