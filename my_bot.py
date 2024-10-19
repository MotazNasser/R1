import nest_asyncio
nest_asyncio.apply()

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Define the response when the bot receives the '/start' command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your bot. How can I help you today?')

# Define the response to any text message
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    await update.message.reply_text(f'You said: {user_message}')

async def main() -> None:
    app = ApplicationBuilder().token('7901330626:AAGLbAn15rRAccFtkDcZi1ast_zBGm0rGhg').build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
