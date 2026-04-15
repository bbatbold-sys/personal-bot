import httpx
from discord.ext import commands


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="weather")
    async def weather(self, ctx, *, city: str = None):
        if not city:
            await ctx.send("Usage: `!weather <city>`\nExample: `!weather London`")
            return

        async with ctx.typing():
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
                    f"**Weather in {location}, {country}**\n\n"
                    f"Condition: {description}\n"
                    f"Temperature: {temp_c}°C (feels like {feels_like}°C)\n"
                    f"Humidity: {humidity}%\n"
                    f"Wind: {wind_kmph} km/h"
                )
                await ctx.send(text)

            except httpx.HTTPStatusError:
                await ctx.send(f"Could not find weather for **{city}**. Check the city name and try again.")
            except Exception:
                await ctx.send("Something went wrong fetching the weather. Please try again.")


async def setup(bot):
    await bot.add_cog(Weather(bot))
