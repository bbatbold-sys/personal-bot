import asyncio
import functools
import io
import os

import discord
import httpx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from discord.ext import commands

FINNHUB_TOKEN = os.getenv("FINNHUB_TOKEN", "")

TICKERS = {
    "AAPL":  "Apple",
    "MSFT":  "Microsoft",
    "GOOGL": "Google",
    "AMZN":  "Amazon",
    "TSLA":  "Tesla",
    "META":  "Meta",
    "NVDA":  "Nvidia",
}

GOLD_SYMBOL = "OANDA:XAU_USD"


def _fetch():
    results = []
    with httpx.Client(timeout=10) as client:
        # Fetch stocks
        for symbol, name in TICKERS.items():
            try:
                r = client.get(
                    "https://finnhub.io/api/v1/quote",
                    params={"symbol": symbol, "token": FINNHUB_TOKEN},
                )
                data = r.json()
                price = data["c"]
                prev = data["pc"]
                if not price or not prev:
                    continue
                change_pct = ((price - prev) / prev) * 100
                results.append((symbol, name, price, change_pct))
            except Exception as e:
                print(f"Failed to fetch {symbol}: {e}")

        # Fetch Gold
        try:
            r = client.get(
                "https://finnhub.io/api/v1/quote",
                params={"symbol": GOLD_SYMBOL, "token": FINNHUB_TOKEN},
            )
            data = r.json()
            price = data["c"]
            prev = data["pc"]
            if price and prev:
                change_pct = ((price - prev) / prev) * 100
                results.append(("XAU/USD", "Gold", price, change_pct))
        except Exception as e:
            print(f"Failed to fetch Gold: {e}")

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
                    lines.append(
                        f"**{symbol}** {name}: `${price:,.2f}` {arrow} {sign}{change_pct:.2f}%"
                    )

                buf = await loop.run_in_executor(None, functools.partial(_build_chart, results))
                await ctx.send("\n".join(lines), file=discord.File(buf, filename="stocks.png"))

            except Exception as e:
                print(f"Stock error: {e}")
                await ctx.send(f"Couldn't fetch stock data right now. Error: `{e}`")


async def setup(bot):
    await bot.add_cog(Stock(bot))
