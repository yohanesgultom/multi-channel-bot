import logging
import requests
import time
from . import settings, api_post
from .models import db, RSSNotification

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
    # TODO get from db
    tickers = [
        ['ada_idr', 29364],
        ['eos_idr', 165001],
        ['eth_idr', 0],
        ['dot_idr', 0],
        ['vex_idr', 0],
    ]
    # get current price from indodax
    r = requests.get(f'https://indodax.com/api/summaries')
    data = r.json()
    items = []
    server_time = None
    if 'tickers' not in data:
        print('ERROR: data does not contain tickers')
    else:
        for (t, ref_price) in tickers:
            if t not in data['tickers']:
                print(f'ERROR: {t} not in tickers data')
            else:
                t_data = data['tickers'][t]
                t_name = t_data['name']
                t_last = int(t_data['last'])
                t_change = (t_last - ref_price) / ref_price * 100 if ref_price > 0 else 0
                t_change_sym = '🟢' if t_change >= 0 else '🔴'
                if server_time is None:
                    server_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(t_data['server_time'])))
                items.append(f'{t_change_sym} <b>{t_name}</b>: IDR {t_last:,} ({t_change:,.1f}%)')
    html = '💲 <b>Indodax Summary</b>\n\n' + '\n'.join(items) + f'\n\n⏰️ {server_time}'
    # print(msg)
    notifications = db.session.query(RSSNotification) \
            .order_by(RSSNotification.chat_id) \
            .all()
    for n in notifications:
        msg = {'chat_id': n.chat_id, 'text': html, 'parse_mode': 'HTML'}
        api_post('sendMessage', data=msg)


if __name__ == "__main__":
    # run all functions with @job decorator
    for fname, (f, args) in jobs.items():
        logging.info(f'Running {fname} with {args}..')
        f(*args)
