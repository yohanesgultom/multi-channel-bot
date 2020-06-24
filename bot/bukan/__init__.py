import aiml
import os

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

NAME = 'Bukan'
GENDER = 'Male'
AIML_FILE = os.path.join(CURRENT_DIR, 'aiml', 'std-startup.xml')
AIML_LOAD_CMD = 'load aiml b'

k = aiml.Kernel()
k.learn(AIML_FILE)
k.respond(AIML_LOAD_CMD)
k.setBotPredicate('name', NAME)
k.setBotPredicate('gender', GENDER)

class Bukan:
    def reply(self, msg, user_id=None):
        session_id = k._globalSessionID
        if user_id:
            k._addSession(user_id)
            session_id = user_id
        return k.respond(msg, sessionID=session_id)