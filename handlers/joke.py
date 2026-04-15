import httpx
from discord.ext import commands

JOKE_API_URL = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist,explicit"


class Joke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="joke")
    async def joke(self, ctx):
        async with ctx.typing():
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(JOKE_API_URL, timeout=10)
                    response.raise_for_status()
                    data = response.json()

                if data["type"] == "single":
                    text = data["joke"]
                else:
                    text = f"{data['setup']}\n\n||{data['delivery']}||"

                await ctx.send(text)

            except Exception:
                await ctx.send("Couldn't fetch a joke right now. Try again!")


async def setup(bot):
    await bot.add_cog(Joke(bot))
