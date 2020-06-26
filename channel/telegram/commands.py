import utils.helper as helper
from .models import db, RSSNotification

def rss_add(user_id, chat_id, rss_url):
    # TODO: Premium user?
    limit = 2
    count = db.session.query(RSSNotification.id).count()
    if count >= limit:
        return {'text': 'Sorry, currently we only allow max 2 RSS URLs per user 🙏🏻'}
    notif = RSSNotification(
        user_id=user_id,
        chat_id=chat_id,
        rss_url=rss_url
    )
    db.session.add(notif)
    db.session.commit()
    return {'text': '✅ RSS notification added'}

def rss_list(user_id):
    results = db.session.query(RSSNotification) \
        .filter(RSSNotification.user_id == user_id) \
        .all()
    if len(results) <= 0:
        reply = 'ℹ️ No RSS notification found'
    else:
        reply = '✅ RSS notifications found\n\n'
        reply += '```\n'
        reply += '\n\n'.join([f'ID={r.id}\t URL={helper.str_limit(r.rss_url, 100)}' for r in results])
        reply += '```\n'
    return {'text': reply, 'parse_mode': 'MarkdownV2'}

def rss_del(user_id, id):
    notif = db.session.query(RSSNotification) \
        .filter(RSSNotification.user_id == user_id, RSSNotification.id == id) \
        .first()
    if notif:
        db.session.delete(notif)
        db.session.commit()
        reply = '✅ RSS notification deleted'
    else:
        reply = '⚠️ RSS notification not found'
    return {'text': reply}
