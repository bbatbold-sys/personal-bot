import httpx
from telegram import Update
from telegram.ext import ContextTypes


async def weather_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /weather <city>\nExample: /weather London")
        return

    city = " ".join(context.args)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://wttr.in/{city}?format=j1",
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

        current = data["current_condition"][0]
        area = data["nearest_area"][0]

        location = area["areaName"][0]["value"]
        country = area["country"][0]["value"]
        temp_c = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        description = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]
        wind_kmph = current["windspeedKmph"]

        text = (
            f"Weather in {location}, {country}\n\n"
            f"Condition: {description}\n"
            f"Temperature: {temp_c}°C (feels like {feels_like}°C)\n"
            f"Humidity: {humidity}%\n"
            f"Wind: {wind_kmph} km/h"
        )
        await update.message.reply_text(text)

    except httpx.HTTPStatusError:
        await update.message.reply_text(f"Could not find weather for '{city}'. Check the city name and try again.")
    except Exception:
        await update.message.reply_text("Something went wrong fetching the weather. Please try again.")
