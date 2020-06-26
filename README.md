# Multi-Channel Bot

Multi-channel modular chat bot non-blocking HTTP server

Currently supported channels:

1. Basic: simple channel accepting `POST /basic/` containing `{"message": "your message"}` body
2. Telegram: https://core.telegram.org/bots/api. Demo: https://t.me/saya_bukan_bot

**Future support plan**

1. LINE
2. Facebook
3. Discord
4. Viber

Requirements:

1. Python >= 3.5

Setup local server:

1. Rename `.env.example` to `.env` and modify it accordingly
2. Install requirements `pip install -r requirements.txt`
3. Run server `python server.py`

To test the bot (defined in `.env`) using CLI, run:

```
python cli.py
```

**Testing**

## Testing

Run all tests:

```
python -m unittest discover -v -s test
```

Run any single test:

```
python -m unittest test.unit.test_rss.TestRSS
```

## Channels

Add your own channel by following example below:

### Basic

Basic channel is activated by default if you rename `.env.example` without modifying. 

Interact with the bot by sending HTTP POST such as: 

```
curl --header "Content-Type: application/json" --request POST --data '{"message":"hello"}' http://localhost:3000/basic/
```

### Telegram

To activate telegram channel follow these steps: 

1. Modify `.env`:
   1. Set `CHANNELS=Telegram`
   2. Set `SERVER_URL` with your web server (where this server is deployed)
   3. Set `TELEGRAM_BOT_TOKEN` with [your bot token](https://core.telegram.org/bots#6-botfather)
2. Run server `python server.py`
3. Test by chatting with your bot in Telegram client

## Bot

Add you own bot by adding new directory inside `bot/` and `__init__.py` in it. Checkout existing bots for example:

1. Echo: simple bot that echo your message
2. Bukan: AIML-based bot
