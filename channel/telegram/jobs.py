import logging
from channel.telegram import settings, api_post
from channel.telegram.models import db, RSSNotification, TradingPortfolio
from utils import indodax

LOG_LEVEL = settings.env('LOG_LEVEL', default='WARNING')
logging.basicConfig(level=getattr(logging, LOG_LEVEL))

jobs = {}


def job(func, *func_args):
    jobs[func.__name__] = (func, func_args)

    def w():
        return func()

    return w


@job
def send_indodax_summary():    
    results = db.session.query(TradingPortfolio).all()
    if len(results) <= 0:
        logging.info('ℹ️ No user found')
    else:
        for r in results:
            if r and 'indodax' in r.data:
                html = indodax.get_indodax_summary(r.data['indodax'])
                msg = {'chat_id': r.user_id, 'text': html, 'parse_mode': 'HTML'}
                api_post('sendMessage', data=msg)


if __name__ == "__main__":
    # run all functions with @job decorator
    for fname, (f, args) in jobs.items():
        logging.info(f'Running {fname} with {args}..')
        f(*args)
