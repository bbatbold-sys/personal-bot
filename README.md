# Personal Discord Bot

A Discord bot with three commands: weather lookup, random jokes, and inspirational quotes. Built with `discord.py` and deployed on Railway.

---

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `!hello` | Show help message | `!hello` |
| `!weather <city>` | Current weather for any city | `!weather Tokyo` |
| `!joke` | Random joke (family-friendly) | `!joke` |
| `!quote` | Random inspirational quote | `!quote` |

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

Why don't scientists trust atoms?

||Because they make up everything!||
```

**Quote:**
```
!quote

"The only way to do great work is to love what you do."

— Steve Jobs
```

---

## Setup

### 1. Create a Discord bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application** → give it a name → **Create**
3. Go to **Bot** → click **Add Bot**
4. Under **Token** click **Reset Token** and copy it
5. Under **Privileged Gateway Intents** enable **Message Content Intent**
6. Go to **OAuth2 → URL Generator** → check `bot` scope → check `Send Messages`, `Read Message History` permissions → copy the URL and use it to invite the bot to your server

### 2. Install dependencies

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment

```bash
copy .env.example .env
# Edit .env and paste your token:
# DISCORD_TOKEN=your_token_here
```

### 4. Run locally

```bash
python bot.py
```

---

## Deployment (Railway)

1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app/) and create a new project from your GitHub repo
3. Go to **Variables** → add: `DISCORD_TOKEN = your_token_here`
4. Railway picks up `railway.toml` automatically and deploys

The bot runs as a persistent worker process.

---

## Project Structure

```
personal-bot/
├── bot.py               # Entry point, loads all cogs
├── config.py            # Loads DISCORD_TOKEN from environment
├── handlers/
│   ├── start.py         # !hello command
│   ├── weather.py       # !weather command (wttr.in)
│   ├── joke.py          # !joke command (jokeapi.dev)
│   └── quote.py         # !quote command (quotable.io)
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

No extra accounts needed beyond your Discord bot token.
