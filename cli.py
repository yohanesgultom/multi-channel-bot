from pathlib import Path
import settings
import importlib

bot_name = settings.env('BOT', default='Echo')    
bot_module = importlib.import_module(f'bot.{bot_name.lower()}')
bot_class = getattr(bot_module, bot_name)
bot = bot_class()
print(f'{bot_name} bot loaded')
print('Press Ctrl+C to quit...\n')

print(f'Bot> Hi. What\'s your name?')
user_name = input('You> ')
bot.set_predicate('name', user_name)
reply = bot.reply('Hi')
print(f'Bot> {reply}')

while True:
    try:        
        msg = input('You> ')
        if msg:
            reply = bot.reply(msg)
            print(f'Bot> {reply}')
    except KeyboardInterrupt:
        print('\nBot> bye!')
        break