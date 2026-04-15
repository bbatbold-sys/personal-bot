import discord
from discord.ext import commands
from config import DISCORD_TOKEN

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


async def main():
    async with bot:
        await bot.load_extension("handlers.start")
        await bot.load_extension("handlers.weather")
        await bot.load_extension("handlers.joke")
        await bot.load_extension("handlers.quote")
        await bot.load_extension("handlers.stock")
        try:
            await bot.load_extension("handlers.prediction")
            print("Prediction handler loaded.")
        except Exception as e:
            print(f"Prediction handler skipped (ML deps not available): {e}")
        await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
