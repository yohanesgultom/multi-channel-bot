import unittest
import random

from bot.bukan import Bukan as BukanBot
from bot.echo import Echo as EchoBot

class TestBot(unittest.TestCase):
    messages = ['hello', 'hi', 'what\'s your name?', 'you are cool!', 'i love pasta']

    def test_echo_reply(self):        
        bot = EchoBot()
        msg = random.choices(self.messages)[0]
        reply = bot.reply(msg)
        self.assertEqual(reply, f'you just said: {msg}')

    def test_bukan_reply(self):
        bot = BukanBot()
        msg = random.choices(self.messages)[0]
        reply = bot.reply(msg)
        self.assertTrue(len(reply) > 1)
