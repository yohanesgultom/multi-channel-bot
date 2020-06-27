import aiml
import os
import logging
import settings
from bot.base import Base

LOG_LEVEL = settings.env('LOG_LEVEL', default='WARNING')
logging.basicConfig(level=getattr(logging, LOG_LEVEL))

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

NAME = 'Bukan'
GENDER = 'Male'
AIML_FILE = os.path.join(CURRENT_DIR, 'aiml', 'std-startup.xml')
AIML_LOAD_CMD = 'load aiml b'

class Bukan(Base):
    def __init__(self):
        k = aiml.Kernel()
        k.learn(AIML_FILE)
        k.respond(AIML_LOAD_CMD)
        k.setBotPredicate('name', NAME)
        k.setBotPredicate('gender', GENDER)
        self.k = k

    def reply(self, msg, user_id=None):
        session_id = self.k._globalSessionID
        if user_id:
            self.k._addSession(user_id)
            session_id = user_id   
        return self.k.respond(msg, sessionID=session_id)

    def get_predicate(self, key, user_id=None):
        session_id = user_id if user_id else self.k._globalSessionID
        self.k.getPredicate(key, sessionID=session_id)

    def set_predicate(self, key, val, user_id=None):
        session_id = user_id if user_id else self.k._globalSessionID
        self.k.setPredicate(key, val, sessionID=session_id)
       
