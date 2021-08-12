from aiohttp import web
import requests
import logging

import settings
from channel.basic import Basic
from . import commands


SERVER_URL = settings.env('SERVER_URL')
BOT_TOKEN = settings.env('TELEGRAM_BOT_TOKEN')
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'


class Telegram(Basic):
    def __init__(self, bot): 
        super().__init__(bot)

        # check bot token
        # {"ok":true,"result":{"id":1104292123,"is_bot":true,"first_name":"Bukan Bot","username":"saya_bukan_bot","can_join_groups":true,"can_read_all_group_messages":false,"supports_inline_queries":false}}
        res = api_get('getMe')       
        if not res['ok']:
            raise Exception(f'Invalid BOT_TOKEN: {BOT_TOKEN}')

        # try to set botPredicate
        name_tokens = []
        data = res['result']
        if 'first_name' in data:
            name_tokens.append(data['first_name'])
        if 'last_name' in data:
            name_tokens.append(data['last_name'])
        if name_tokens:            
            bot_name = ' '.join(name_tokens)
            self.bot.k.setBotPredicate('name', bot_name)

        # register webhook
        # {"ok":true,"result":true,"description":"Webhook was set"
        webhook_url = f'{SERVER_URL}/telegram/{BOT_TOKEN}'
        res = api_post('setWebhook', data={ 'url': webhook_url})
        if not res['ok']:
            logging.error(res)
            raise Exception(f'Unable to register webhook: {webhook_url}')
        logging.info(f'Telegram webhook registered: {webhook_url}')

    def routes(self):
        # (method, path, handler)
        return [('POST', f'{BOT_TOKEN}', self.handle)]

    async def handle(self, request):
        reply = '?'

        if request.can_read_body:
            # {'update_id': 45470334, 'message': {'message_id': 384, 'from': {'id': 405179790, 'is_bot': False, 'first_name': 'Yohanes', 'last_name': 'Gultom', 'username': 'yohanesgultom', 'language_code': 'en'}, 'chat': {'id': 405179790, 'first_name': 'Yohanes', 'last_name': 'Gultom', 'username': 'yohanesgultom', 'type': 'private'}, 'date': 1593177484, 'text': '/h', 'entities': [{'offset': 0, 'length': 2, 'type': 'bot_command'}]}}
            body = await request.json()
            logging.debug(body) 
            update_id = body['update_id']

            # message
            message = body['message']
            message_id = message['message_id']
            msg = message['text']

            # message.sender
            sender = message['from']            
            sender_id = sender['id']
            sender_username = sender['username'] if 'username' in sender else None
            sender_first_name = sender['first_name'] if 'first_name' in sender else None

            # message.chat
            chat = message['chat']
            chat_id = chat['id']
            if not sender_username and 'username' in chat:
                sender_username = chat['username']
            if not sender_first_name and 'first_name' in chat:
                sender_first_name = chat['first_name']

            # set name if not yet done
            if not self.bot.get_predicate('name', user_id=sender_id):
                name = sender_first_name if sender_first_name else sender_username
                self.bot.set_predicate('name', name, user_id=sender_id)
            
            # get reply
            reply = {'chat_id': chat_id}
            if msg.startswith('/'):
                tokens = msg.split()
                cmd = tokens[0].split('/')[-1]
                args = tokens[1:]
                cmd_reply = self.execute(cmd, sender_id, chat_id, *args)
                reply.update(cmd_reply)
            else:
                bot_reply = {'text': self.bot.reply(msg, user_id=sender_id)}
                reply.update(bot_reply)
                    
            # send chat to telegram
            # {"ok":true,"result":{"message_id":385,"from":{"id":1104292123,"is_bot":true,"first_name":"Bukan Bot","username":"saya_bukan_bot"},"chat":{"id":405179790,"first_name":"Yohanes","last_name":"Gultom","username":"yohanesgultom","type":"private"},"date":1593177528,"text":"\u2139\ufe0f Available commands:\n\n`/rss_add url` : Add new RSS URL to monitor\n\n`/rss_list` : List monitored RSS URLs\n\n`/rss_del id` : Remove monitored RSS URL by ID","entities":[{"offset":25,"length":8,"type":"bot_command"},{"offset":70,"length":9,"type":"bot_command"},{"offset":109,"length":8,"type":"bot_command"}]}}
            res = api_post('sendMessage', data=reply)

        return web.json_response({'message': reply})

    def execute(self, cmd, sender_id, chat_id, *args):
        reply = {'text': 'Sorry, I don\'t understand your command 😟'}
        # TODO: use decoration and reflection
        # to automatically register and map commands
        try:
            if cmd in ['h', 'help', 'start']:
                bot_name = self.bot.k.getBotPredicate('name')
                creator = '@yohanesgultom'
                reply.update(commands.get_help(bot_name, creator))
            elif cmd == 'rss_add':
                reply.update(commands.rss_add(sender_id, chat_id, args[0]))
            elif cmd == 'rss_list':
                reply.update(commands.rss_list(sender_id))
            elif cmd == 'rss_del':
                reply.update(commands.rss_del(sender_id, args[0]))
            elif cmd == 'indodax':
                reply.update(commands.indodax())
            elif cmd == 'indodax_add':
                if len(args) < 2:
                    reply.update({'text': '⚠️ Usage: `indodax_add <PAIR> <BUY PRICE>`\nExample: `indodax_add ada_idr 25600`', 'parse_mode': 'MarkdownV2'})
                else:
                    reply.update(commands.trading_portfolio_add(sender_id, 'indodax', args[0], args[1]))
            elif cmd == 'indodax_del':
                if len(args) < 2:
                    reply.update({'text': '⚠️ Usage: `indodax_del <PAIR>`\nExample: `indodax_del ada_idr`', 'parse_mode': 'MarkdownV2'})
                else:
                    reply.update(commands.trading_portfolio_del(sender_id, 'indodax', args[0]))
        except Exception as e:
            logging.exception(e)
        return reply


def api_get(path, data={}):
    r = requests.get(f'{BASE_URL}/{path}', params=data)
    logging.debug(r.text)
    return r.json()


def api_post(path, data={}):
    r = requests.post(f'{BASE_URL}/{path}', json=data)
    logging.debug(r.text)
    return r.json()
