import httpx
from discord.ext import commands

JOKE_API_URL = "https://icanhazdadjoke.com/"


class Joke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="joke")
    async def joke(self, ctx):
        async with ctx.typing():
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        JOKE_API_URL,
                        headers={"Accept": "application/json"},
                        timeout=10,
                    )
                    response.raise_for_status()
                    data = response.json()

                await ctx.send(data["joke"])

            except Exception as e:
                print(f"Joke error: {e}")
                await ctx.send("Couldn't fetch a joke right now. Try again!")


async def setup(bot):
    await bot.add_cog(Joke(bot))
