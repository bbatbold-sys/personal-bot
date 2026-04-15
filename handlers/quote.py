import httpx
from discord.ext import commands

QUOTE_API_URL = "https://api.quotable.io/random"


class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="quote")
    async def quote(self, ctx):
        async with ctx.typing():
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(QUOTE_API_URL, timeout=10)
                    response.raise_for_status()
                    data = response.json()

                text = f'*"{data["content"]}"*\n\n— **{data["author"]}**'
                await ctx.send(text)

            except Exception:
                await ctx.send("Couldn't fetch a quote right now. Try again!")


async def setup(bot):
    await bot.add_cog(Quote(bot))
