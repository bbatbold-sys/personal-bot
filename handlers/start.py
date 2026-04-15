from telegram import Update
from telegram.ext import ContextTypes


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Hello! I'm your personal bot. Here's what I can do:\n\n"
        "/weather <city> — Current weather for any city\n"
        "/joke — Random joke\n"
        "/quote — Random inspirational quote\n"
    )
    await update.message.reply_text(text)
