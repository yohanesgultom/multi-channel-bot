import time
import logging
import settings
from datetime import datetime, timezone
from utils.rss import RSSParser
from . import api_post
from .models import db, RSSNotification

LOG_LEVEL = settings.env('LOG_LEVEL', default='WARNING')
logging.basicConfig(level=getattr(logging, LOG_LEVEL))

jobs = {}
def job(f, *args):
    jobs[f.__name__] = (f, args)
    def w():        
        return f
    return w

@job
def send_notif(limit_per_person=5, message_delay=5):
    """
    Iterate all RSS notification records, fetch the RSS feed
    Send every new item to the corresponding chat_id
    """
    now = datetime.now(timezone.utc)
    notifs = db.session.query(RSSNotification) \
        .order_by(RSSNotification.chat_id) \
        .all()
    parser = RSSParser()
    for n in notifs:
        try:
            items = parser.fetch(n.rss_url, last_update=n.last_item_date)
            if items:
                # send notif
                max_date = n.last_item_date
                limit = min(limit_per_person, len(items))
                renderer = render_common
                if n.rss_url.startswith('https://www.upwork.com'):
                    renderer = render_upwork
                count = 0
                for item in items:
                    msg = renderer(item, n)
                    if msg:
                        res = api_post('sendMessage', data=msg)
                        # track max date
                        if 'pubDate' in item:
                            max_date = max(max_date, item['pubDate']) \
                                if max_date else item['pubDate']
                        logging.debug(res)
                        time.sleep(message_delay)
                        count += 1
                        if count >= limit:
                            break
                n.last_item_date = max_date
                db.session.commit()                
        except Exception as e:
            logging.error(f'Failed sending notif for #{n.id}: {n.rss_url}')
            logging.exception(e)

def render_common(item, n):
    s = ""
    # title
    if 'title' in item:
        s += f"<b>{item['title']}</b>\n\n"
    # description
    if 'description' in item:
        s += f"{item['description']}\n"
    elif 'content:encoded' in item:
        s += f"{item['content:encoded']}\n"
    return {'chat_id': n.chat_id, 'text': s, 'parse_mode': 'HTML'} \
        if s else None

def render_upwork(item, n):
    s = ""    
    if 'title' in item:
        # TODO: get criteria from database
        if (not item['title'].lower().startswith('do not apply')) \
            and (not item['rate_high'] or item['rate_high'] >= 20) \
            and (not item['country'] or item['country'].lower() not in ['india', 'pakistan', 'bangladesh']):

            s += f"<b>{item['title']}</b>\n\n"
            description = None
            if 'description' in item:
                description = item['description']
            elif 'encoded' in item:
                description = item['encoded']
            s += f"{description}\n"
    return {'chat_id': n.chat_id, 'text': s, 'parse_mode': 'HTML'} \
        if s else None


if __name__ == "__main__":
    # run all functions with @job decorator
    for fname, (f, args) in jobs.items():
        logging.info(f'Running {fname} with {args}..')
        f(*args)
