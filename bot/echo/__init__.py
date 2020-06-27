from bot.base import Base

class Echo(Base):
    def reply(self, msg, user_id=None):
        return f'you just said: {msg}'
