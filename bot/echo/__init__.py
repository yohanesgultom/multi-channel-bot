import bot

class Echo(bot.Base):
    def reply(self, msg, user_id=None):
        return f'you just said: {msg}'
