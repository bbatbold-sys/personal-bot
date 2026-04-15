import httpx
from telegram import Update
from telegram.ext import ContextTypes

QUOTE_API_URL = "https://api.quotable.io/random"


async def quote_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(QUOTE_API_URL, timeout=10)
            response.raise_for_status()
            data = response.json()

        text = f'"{data["content"]}"\n\n— {data["author"]}'
        await update.message.reply_text(text)

    except Exception:
        await update.message.reply_text("Couldn't fetch a quote right now. Try again!")
