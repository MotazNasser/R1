import nest_asyncio
from telethon import TelegramClient, events
import uuid
import asyncio

# Allow nested event loops
nest_asyncio.apply()

# Replace with your actual values
api_id = 20012903  # Your actual API ID (as an integer)
api_hash = '5abe0773880d98a9ee6d14ca7d7e988e'  # Your actual API Hash (keep it as a string)
bot_token = '7901330626:AAGLbAn15rRAccFtkDcZi1ast_zBGm0rGhg'  # Your actual Bot Token (keep it as a string)

async def main():
    # Create a unique session name using UUID to prevent locking issues
    session_name = str(uuid.uuid4())
    client = TelegramClient(session_name, api_id, api_hash)

    # Start the client using the bot token
    await client.start(bot_token=bot_token)

    print("Bot is running and listening for forwarded messages...")  # Debug message

    # Listen for new messages sent to the bot
    @client.on(events.NewMessage())  # Listen for any new messages
    async def handler(event):
        message_text = event.message.message
        print(f"Received forwarded message: {message_text}")  # Print received message

        # Here you can parse the message for trading signals
        parse_trading_signal(message_text)

    # Run the client until you stop it
    await client.run_until_disconnected()

def parse_trading_signal(message):
    # Implement your signal parsing logic here
    print(f"Parsing signal: {message}")

# Start the client
if __name__ == "__main__":
    asyncio.run(main())
