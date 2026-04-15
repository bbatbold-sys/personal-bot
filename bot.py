from telegram.ext import ApplicationBuilder, CommandHandler
from config import BOT_TOKEN
from handlers.start import start_handler
from handlers.weather import weather_handler
from handlers.joke import joke_handler
from handlers.quote import quote_handler


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("weather", weather_handler))
    app.add_handler(CommandHandler("joke", joke_handler))
    app.add_handler(CommandHandler("quote", quote_handler))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
