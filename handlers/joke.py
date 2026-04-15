import httpx
from telegram import Update
from telegram.ext import ContextTypes

JOKE_API_URL = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist,explicit"


async def joke_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(JOKE_API_URL, timeout=10)
            response.raise_for_status()
            data = response.json()

        if data["type"] == "single":
            text = data["joke"]
        else:
            text = f"{data['setup']}\n\n{data['delivery']}"

        await update.message.reply_text(text)

    except Exception:
        await update.message.reply_text("Couldn't fetch a joke right now. Try again!")
