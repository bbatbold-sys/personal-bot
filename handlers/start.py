from discord.ext import commands


class Start(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help_bot", aliases=["hello"])
    async def help_bot(self, ctx):
        text = (
            "**Personal Bot — Commands**\n\n"
            "`!weather <city>` — Current weather for any city\n"
            "`!joke` — Random joke\n"
            "`!quote` — Random inspirational quote\n"
        )
        await ctx.send(text)


async def setup(bot):
    await bot.add_cog(Start(bot))
