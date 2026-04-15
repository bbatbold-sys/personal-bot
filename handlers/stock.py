import asyncio
import functools
import io

import discord
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import yfinance as yf
from discord.ext import commands

TICKERS = {
    "AAPL":  "Apple",
    "MSFT":  "Microsoft",
    "GOOGL": "Google",
    "AMZN":  "Amazon",
    "TSLA":  "Tesla",
    "META":  "Meta",
    "NVDA":  "Nvidia",
    "GC=F":  "Gold",
}


def _fetch():
    results = []
    for symbol, name in TICKERS.items():
        try:
            fi = yf.Ticker(symbol).fast_info
            price = fi.last_price
            prev = fi.previous_close
            change_pct = ((price - prev) / prev) * 100
            results.append((symbol, name, price, change_pct))
        except Exception:
            pass
    return results


def _build_chart(results):
    labels = [r[0] for r in results]
    changes = [r[3] for r in results]
    colors = ["#2ecc71" if c >= 0 else "#e74c3c" for c in changes]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(labels, changes, color=colors, height=0.6)
    ax.axvline(0, color="#aaaaaa", linewidth=0.8)

    for bar, val in zip(bars, changes):
        ax.text(
            val + (0.05 if val >= 0 else -0.05),
            bar.get_y() + bar.get_height() / 2,
            f"{'+' if val >= 0 else ''}{val:.2f}%",
            va="center",
            ha="left" if val >= 0 else "right",
            color="white",
            fontsize=9,
        )

    ax.set_xlabel("% Change today", color="white", fontsize=10)
    ax.set_title("Stock & Gold — Daily % Change", color="white", fontsize=12, pad=12)
    ax.tick_params(colors="white")
    ax.set_facecolor("#2c2f33")
    fig.patch.set_facecolor("#2c2f33")
    for spine in ax.spines.values():
        spine.set_edgecolor("#555555")

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=130, bbox_inches="tight")
    buf.seek(0)
    plt.close()
    return buf


class Stock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stock")
    async def stock(self, ctx):
        async with ctx.typing():
            try:
                loop = asyncio.get_event_loop()
                results = await loop.run_in_executor(None, functools.partial(_fetch))

                if not results:
                    await ctx.send("Couldn't fetch stock data right now. Try again!")
                    return

                lines = ["**Stock & Gold Prices**\n"]
                for symbol, name, price, change_pct in results:
                    arrow = "↑" if change_pct >= 0 else "↓"
                    sign = "+" if change_pct >= 0 else ""
                    unit = "oz" if symbol == "GC=F" else ""
                    lines.append(
                        f"**{symbol}** {name}: `${price:,.2f}{f'/{unit}' if unit else ''}` {arrow} {sign}{change_pct:.2f}%"
                    )

                buf = await loop.run_in_executor(None, functools.partial(_build_chart, results))
                await ctx.send("\n".join(lines), file=discord.File(buf, filename="stocks.png"))

            except Exception as e:
                print(f"Stock error: {e}")
                await ctx.send("Couldn't fetch stock data right now. Try again!")


async def setup(bot):
    await bot.add_cog(Stock(bot))
