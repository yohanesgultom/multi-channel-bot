from aiohttp import web
from channel.basic import Basic
import requests
import settings
import logging

SERVER_URL = settings.env('SERVER_URL')
BOT_TOKEN = settings.env('TELEGRAM_BOT_TOKEN')
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

class Telegram(Basic):
    def __init__(self, bot): 
        super().__init__(bot)

        # check bot token
        res = self.api_get('getMe')
        if not res['ok']:
            raise Exception(f'Invalid BOT_TOKEN: {BOT_TOKEN}')

        # register webhook
        webhook_url = f'{SERVER_URL}/telegram/{BOT_TOKEN}'
        res = self.api_post('setWebhook', data={ 'url': webhook_url})
        if not res['ok']:
            logging.error(res)
            raise Exception(f'Unable to register webhook: {webhook_url}')
        logging.info(f'Telegram webhook registered: {webhook_url}')

    async def handle(self, request):
        reply = '?'

        if request.can_read_body:
            body = await request.json()
            logging.debug(body) 
            update_id = body['update_id']
            message = body['message']
            message_id = message['message_id']
            chat = message['chat']
            chat_id = chat['id']
            sender = body['message']['from']            
            sender_id = sender['id']
            sender_username = sender['username']
            msg = body['message']['text']
            reply = self.bot.reply(msg, user_id=sender_id)
        
            # send chat to telegram
            # TODO: maintain bot session           
            res = self.api_post('sendMessage', data={'chat_id': chat_id, 'text': reply})
            logging.debug(res)

        return web.json_response({'message': reply})

    def routes(self):
        # (method, path, handler)
        return [('POST', f'{BOT_TOKEN}', self.handle)]

    def api_get(self, path, data={}):
        r = requests.get(f'{BASE_URL}/{path}', params=data)
        return r.json()

    def api_post(self, path, data={}):
        r = requests.post(f'{BASE_URL}/{path}', json=data)
        return r.json()