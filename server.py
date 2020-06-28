from aiohttp import web
from pathlib import Path
import settings
import importlib
import logging

LOG_LEVEL = settings.env('LOG_LEVEL', default='WARNING')
logging.basicConfig(level=getattr(logging, LOG_LEVEL))

async def handle(request):
    return web.json_response({'message': 'hello world'})
    
@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        return response
    except Exception as e:
        logging.exception(e)
        return web.Response(text=str(e), status=500)

def channel_routes():
    routes = {}

    bot_name = settings.env('BOT', default='Echo')    
    bot_module = importlib.import_module(f'bot.{bot_name.lower()}')
    bot_class = getattr(bot_module, bot_name)
    bot = bot_class()

    channel_names = settings.env('CHANNELS', default='Basic')
    for channel_name in channel_names.split(','):
        channel_module = importlib.import_module(f'channel.{channel_name.lower()}')
        channel_class = getattr(channel_module, channel_name)
        channel = channel_class(bot)
        for method, route, handler in channel.routes():
            scoped_route = f'/{channel_name.lower()}/{route}'
            if scoped_route in routes:
                raise RuntimeError(f'Conflicting channel route: {scoped_route}')            
            if method == 'GET':
                routes[scoped_route] = web.get(scoped_route, handler)
            elif method == 'POST':
                routes[scoped_route] = web.post(scoped_route, handler)
            else:
                raise RuntimeError(f'Unsupported method defined for {scoped_route}: {method}')
            logging.info(f'Route registered: {method} {scoped_route}')

    return routes.values()

# application
app = web.Application(middlewares=[error_middleware])
routes = [
    web.get('/', handle),
]
routes += channel_routes()
app.add_routes(routes)

if __name__ == '__main__':    
    web.run_app(app, port=settings.env('SERVER_PORT', 5000))