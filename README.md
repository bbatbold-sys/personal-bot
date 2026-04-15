# Personal Discord Bot

A Discord bot with five commands: weather lookup, dad jokes, inspirational quotes, live stock prices with charts, and AI-powered stock predictions. Built with `discord.py` and deployed on Railway.

---

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `!hello` | Show help message | `!hello` |
| `!weather <city>` | Current weather for any city | `!weather Tokyo` |
| `!joke` | Random dad joke | `!joke` |
| `!quote` | Random inspirational quote | `!quote` |
| `!stock` | Live prices + daily % change chart for top stocks and gold | `!stock` |
| `!prediction <ticker>` | AI BUY/SELL/HOLD prediction from latest news (local only) | `!prediction NVDA` |

> **Note:** `!prediction` uses FinBERT + XGBoost ML models and runs locally only. All other commands are deployed and always available.

---

## Example Interactions

**Weather:**
```
!weather Paris

Weather in Paris, France
Condition: Partly Cloudy
Temperature: 18°C (feels like 16°C)
Humidity: 65%
Wind: 14 km/h
```

**Joke:**
```
!joke

Why don't eggs tell jokes? They'd crack each other up.
```

**Quote:**
```
!quote

"The only way to do great work is to love what you do."
— Steve Jobs
```

**Stock:**
```
!stock
→ Sends live prices + bar chart image showing daily % change for
  AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA, and Gold
```

**Prediction:**
```
!prediction NVDA
→ Fetches latest NVDA news headline, runs FinBERT sentiment +
  XGBoost model, returns BUY/SELL/HOLD with T+1/T+3/T+5 forecasts
```

---

## Setup

### 1. Create a Discord bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application** → give it a name → **Create**
3. Go to **Bot** → **Reset Token** → copy it
4. Enable **Message Content Intent** under Privileged Gateway Intents
5. Go to **OAuth2 → URL Generator** → check `bot` → check `Send Messages`, `Read Message History`, `View Channels`, `Embed Links` → copy URL → invite bot to your server

### 2. Install dependencies

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment

```bash
copy .env.example .env
# Edit .env:
# DISCORD_TOKEN=your_token_here
```

### 4. Run locally

```bash
python bot.py
```

---

## Deployment (Railway)

1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app/) → **New Project** → **Deploy from GitHub repo**
3. Select `personal-bot`
4. Go to **Variables** → add `DISCORD_TOKEN = your_token_here`
5. Railway auto-deploys using `railway.toml`

The bot runs as a persistent worker — no webhook needed.

---

## Project Structure

```
personal-bot/
├── bot.py                  # Entry point, loads all handlers
├── config.py               # Loads DISCORD_TOKEN from environment
├── handlers/
│   ├── start.py            # !hello
│   ├── weather.py          # !weather (wttr.in)
│   ├── joke.py             # !joke (icanhazdadjoke.com)
│   ├── quote.py            # !quote (zenquotes.io)
│   ├── stock.py            # !stock (yfinance + matplotlib chart)
│   └── prediction.py       # !prediction (FinBERT + XGBoost, local only)
├── requirements.txt
├── Procfile
├── railway.toml
└── .env.example
```

---

## APIs & Libraries Used

| Command | Source | API Key? |
|---------|--------|----------|
| `!weather` | wttr.in | No |
| `!joke` | icanhazdadjoke.com | No |
| `!quote` | zenquotes.io | No |
| `!stock` | Yahoo Finance (yfinance) | No |
| `!prediction` | Yahoo Finance + FinBERT + XGBoost | No |

---

## Git Workflow

- Feature branches: `feature/weather-command`, `feature/joke-command`, `feature/quote-command`, `feature/stock-command`
- Git worktrees used for parallel development of weather and joke commands
- GitHub issues tracked per command (#1–#5)
