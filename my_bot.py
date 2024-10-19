import logging
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Apply nest_asyncio
nest_asyncio.apply()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your bot. How can I assist you?')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

async def main() -> None:
    app = ApplicationBuilder().token('7901330626:AAGLbAn15rRAccFtkDcZi1ast_zBGm0rGhg').build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
