import logging
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from binance.client import Client
import os  # To use environment variables for sensitive information

# Apply nest_asyncio
nest_asyncio.apply()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get your Binance API key and secret from environment variables
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')

# Initialize the Binance client
binance_client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your bot. How can I assist you?')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

async def get_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Get account information
        account_info = binance_client.get_account()
        balances = account_info['balances']
        
        # Create a response string with the balances
        balance_message = "Your Binance Balance:\n"
        for asset in balances:
            free_balance = asset['free']
            if float(free_balance) > 0:
                balance_message += f"{asset['asset']}: {free_balance}\n"
        
        if balance_message == "Your Binance Balance:\n":
            balance_message = "You have no balances."

        await update.message.reply_text(balance_message)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def main() -> None:
    app = ApplicationBuilder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_handler(CommandHandler("balance", get_balance))

    # Run the bot
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
