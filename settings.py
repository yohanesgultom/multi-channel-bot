from dotenv import load_dotenv
import os

load_dotenv(verbose=True)


def env(key, default=None):
    val = os.getenv(key)
    return val if val else default
