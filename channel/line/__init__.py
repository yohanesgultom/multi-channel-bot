from aiohttp import web
import asyncio
import requests
import logging
import base64
import hashlib
import hmac

from channel.basic import Basic
import settings

LINE_CHANNEL_SECRET = settings.env('LINE_CHANNEL_SECRET')
LINE_ACCESS_TOKEN = settings.env('LINE_ACCESS_TOKEN')
BASE_URL = f'https://api.line.me/v2'
DEFAULT_HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {LINE_ACCESS_TOKEN}',
}

class Line(Basic):
    def __init__(self, bot): 
        super().__init__(bot)

    def routes(self):
        # (method, path, handler)
        return [('POST', '', self.handle)]

    async def handle(self, request):
        reply = '?'

        if request.can_read_body:
            # validate signature
            body = await request.text()
            body_hmac = hmac.new(
                LINE_CHANNEL_SECRET.encode('utf-8'),
                body.encode('utf-8'), 
                hashlib.sha256
            ).digest()
            signature = base64.b64encode(body_hmac).decode('utf-8')
            logging.debug(f'signature={signature}') 
            logging.debug(f"X-Line-Signature={request.headers['X-Line-Signature']}") 
            if 'X-Line-Signature' not in request.headers \
                or request.headers['X-Line-Signature'] != signature:
                return web.Response(text='Invalid signature', status=401)

            # process events
            body = await request.json()
            logging.debug(body)
            asyncio.ensure_future(self.process_events(body))
        
        return web.json_response({'message': reply})

    async def process_events(self, body): 
        # follow
        # {'events': [{'type': 'follow', 'replyToken': '14f634a5996b45d3ad96172a067fedc4', 'source': {'userId': 'Ucbf8b3fe065b802e3cfec4073aa15872', 'type': 'user'}, 'timestamp': 1593353896965, 'mode': 'active'}], 'destination': 'Ub61cad364b704d060de1793155c2f28d'}            

        # message
        # {'events': [{'type': 'message', 'replyToken': '97aa16dfc2324b27a06600191a1bedc2', 'source': {'userId': 'Ucbf8b3fe065b802e3cfec4073aa15872', 'type': 'user'}, 'timestamp': 1593353956666, 'mode': 'active', 'message': {'type': 'text', 'id': '12225277252413', 'text': 'Hello'}}], 'destination': 'Ub61cad364b704d060de1793155c2f28d'}

        for event in body['events']:
            source = event['source']

            # fetch and set user's name
            user_id = None
            user_name = None
            if source['type'] == 'user':
                user_id = source['userId']
                user_name = self.bot.get_predicate('name', user_id=user_id)
                if not user_name:
                    res = api_get(f'bot/profile/{user_id}')
                    if 'displayName' in res:
                        user_name = res['displayName']
                        self.bot.set_predicate('name', user_name, user_id=user_id)                   

            # reply to user           
            if user_id:
                reply = None
                if event['type'] == 'follow':
                    msg = "Hi. Nice to meet you! 👋🏻"
                    if user_name:
                        msg = f"Hi {user_name}! 👋🏻"
                    reply = {
                        "replyToken": event['replyToken'],
                        "messages": [{ "type": "text", "text": msg }]
                    }
                elif event['type'] == 'message':                
                    msg = event['message']['text']
                    bot_reply = self.bot.reply(msg, user_id=source['userId'])
                    reply = {
                        "replyToken": event['replyToken'],
                        "messages": [{ "type": "text", "text": bot_reply }]
                    }
                if reply:
                    res = api_post('bot/message/reply', data=reply)


def api_get(path, data={}, headers={}):
    headers.update(DEFAULT_HEADERS)
    r = requests.get(f'{BASE_URL}/{path}', params=data, headers=headers)
    logging.debug(r.text)
    return r.json()

def api_post(path, data={}, headers={}):
    headers.update(DEFAULT_HEADERS)
    logging.debug(data)
    r = requests.post(f'{BASE_URL}/{path}', json=data, headers=headers)
    logging.debug(r.text)
    return r.json()
