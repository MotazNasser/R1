import logging
import telegram
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

# Your credentials
BOT_TOKEN = '7901330626:AAGLbAn15rRAccFtkDcZi1ast_zBGm0rGhg'  # Replace this with your actual bot token

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Change to INFO or DEBUG for detailed logs
)
logger = logging.getLogger(__name__)

# Define a simple message handler function
async def message_handler(update: Update, context) -> None:
    text = update.message.text
    logger.info(f"Received message: {text}")  # Log received message
    await update.message.reply_text("What do you want from me?")  # Send a reply

# Main function to start the bot
async def main():
    # Initialize the bot application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add a message handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    logger.info("Bot started and polling for updates...")
    await application.start()  # Start the bot
    await application.updater.start_polling()  # Polling for updates
    await application.updater.idle()  # Keep the bot running until interrupted

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())  # Use asyncio to run the bot
