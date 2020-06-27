# Multi-Channel Bot

Multi-channel chatbot boilerplate using non-blocking HTTP server. 

Features:
* Automatically load all channel defined on `CHANNELS` (comma separated) in `.env`
* Automatically load bot set on `BOT` in `.env`
* Non-blocking HTTP server to serve bot using `aiohttp`
* Test bot using CLI

Currently supported channels:
1. Basic: simple channel accepting `POST /basic/` containing `{"message": "your message"}` body
2. Telegram: https://core.telegram.org/bots/api. Demo: https://t.me/saya_bukan_bot

Future support plan:
1. LINE
2. Facebook
3. Discord
4. Viber

## Development

Requirements:

1. Python >= 3.5

Setup local server:

1. Rename `.env.example` to `.env` and modify it accordingly
2. Install requirements `pip install -r requirements.txt`
3. Run server `python server.py`

To interactively test the bot (defined in `.env`) using CLI, run:

```
python cli.py
```

## Testing

Run all tests:

```
python -m unittest discover -v -s test
```

Run any single test:

```
python -m unittest test.unit.test_rss.TestRSS
```
