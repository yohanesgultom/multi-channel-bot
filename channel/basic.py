from aiohttp import web


class Basic:
    def __init__(self, bot): 
        self.bot = bot

    async def handle(self, request):
        msg = ''
        if request.can_read_body:
            body = await request.json()
            msg = body['message']
        reply = self.bot.reply(msg)
        return web.json_response({'message': reply})

    def routes(self):
        # (method, path, handler)
        return [('POST', '', self.handle)]