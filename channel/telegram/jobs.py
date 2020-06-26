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
def send_notif(limit_per_person=5):
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
                limit = min(limit_per_person, len(items))
                for item in items[:limit]:
                    s = ""
                    # title
                    if 'title' in item:
                        s += f"<b>{item['title']}</b>\n\n"
                    # description
                    if 'description' in item:
                        s += f"{item['description']}\n"
                    elif 'content:encoded' in item:
                        s += f"{item['content:encoded']}\n"
                    # send to user
                    msg = {'chat_id': n.chat_id, 'text': s, 'parse_mode': 'HTML'}
                    res = api_post('sendMessage', data=msg)
                    logging.debug(res)
                    n.last_item_date = item['pubDate'] if 'pubDate' in item else now
                    db.session.commit()
                    time.sleep(5)
        except Exception as e:
            logging.error(f'Failed sending notif for #{n.id}: {n.rss_url}')
            logging.exception(e)

if __name__ == "__main__":
    for fname, (f, args) in jobs.items():
        logging.info(f'Running {fname} with {args}..')
        f(*args)
