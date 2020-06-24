# Multi-Channel Bot

Multi-channel bot server

Requirements:

1. Python >= 3.5

Simple setup:

1. Rename `.env.example` to `.env` and modify it accordingly
2. Install requirements `pip install -r requirements.txt`
3. Run server `python server.py`

> Default `.env` will run `Echo` bot on `Basic` channel on `http://localhost:3000`. Interact with the bot by sending HTTP POST `curl --header "Content-Type: application/json" --request POST --data '{"message":"hello"}' http://localhost:3000/basic/`

## Telegram

To activate telegram channel follow these steps: 
1. Modify `.env`:
   1. Set `CHANNELS=Telegram`
   2. Set `SERVER_URL` with your web server (where this server is deployed)
   3. Set `TELEGRAM_BOT_TOKEN` with [your bot token](https://core.telegram.org/bots#6-botfather)
2. Run server `python server.py`
3. Test by chatting with your bot in Telegram client