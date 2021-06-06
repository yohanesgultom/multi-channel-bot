import logging
from channel.telegram import settings, api_post
from channel.telegram.models import db, RSSNotification
from utils import indodax

LOG_LEVEL = settings.env('LOG_LEVEL', default='WARNING')
logging.basicConfig(level=getattr(logging, LOG_LEVEL))

jobs = {}


def job(func, *func_args):
    jobs[func.__name__] = (func, func_args)

    def w():
        return func

    return w


@job
def send_indodax_summary():
    html = indodax.get_indodax_summary()
    notifications = db.session.query(RSSNotification).order_by(RSSNotification.chat_id).all()
    for n in notifications:
        msg = {'chat_id': n.chat_id, 'text': html, 'parse_mode': 'HTML'}
        api_post('sendMessage', data=msg)


if __name__ == "__main__":
    # run all functions with @job decorator
    for fname, (f, args) in jobs.items():
        logging.info(f'Running {fname} with {args}..')
        f(*args)
