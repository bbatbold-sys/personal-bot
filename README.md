# Personal Telegram Bot

A Telegram bot with three commands: weather lookup, random jokes, and inspirational quotes. Built with `python-telegram-bot` and deployed on Railway.

---

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Show help message | `/start` |
| `/weather <city>` | Current weather for any city | `/weather Tokyo` |
| `/joke` | Random joke (family-friendly) | `/joke` |
| `/quote` | Random inspirational quote | `/quote` |

---

## Example Interactions

**Weather:**
```
/weather Paris

Weather in Paris, France

Condition: Partly Cloudy
Temperature: 18°C (feels like 16°C)
Humidity: 65%
Wind: 14 km/h
```

**Joke:**
```
/joke

Why don't scientists trust atoms?

Because they make up everything!
```

**Quote:**
```
/quote

"The only way to do great work is to love what you do."

— Steve Jobs
```

---

## Setup

### 1. Get a bot token

1. Open Telegram and message [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow the prompts
3. Copy the token you receive

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env and paste your token:
# BOT_TOKEN=your_token_here
```

### 4. Run locally

```bash
python bot.py
```

---

## Deployment (Railway)

1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app/) and create a new project from your repo
3. Add environment variable: `BOT_TOKEN = your_token_here`
4. Railway picks up `railway.toml` automatically and deploys

The bot runs as a persistent worker process — no webhook setup needed.

---

## Project Structure

```
personal-bot/
├── bot.py               # Entry point, registers all handlers
├── config.py            # Loads BOT_TOKEN from environment
├── handlers/
│   ├── start.py         # /start command
│   ├── weather.py       # /weather command (wttr.in)
│   ├── joke.py          # /joke command (jokeapi.dev)
│   └── quote.py         # /quote command (quotable.io)
├── requirements.txt
├── Procfile             # For Heroku-compatible platforms
├── railway.toml         # Railway deployment config
└── .env.example         # Environment variable template
```

---

## APIs Used

- **Weather**: [wttr.in](https://wttr.in/) — no API key required
- **Jokes**: [jokeapi.dev](https://jokeapi.dev/) — no API key required
- **Quotes**: [quotable.io](https://quotable.io/) — no API key required

No extra accounts needed beyond your Telegram bot token.
