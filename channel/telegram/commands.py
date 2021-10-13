import utils.helper as helper
from channel.telegram.models import db, flag_modified, RSSNotification, TradingPortfolio
from utils import ssl, indodax


def get_help(bot_name, creator):
    s = f'🤖 Hi, I am {bot_name}, created by {creator} to reply any of your message\\. I can only do few simple commands below now\\. Hopefully my creator will upgrade me soon\\.\n\n'
    s += 'ℹ️ Available commands:\n\n'
    s += '* `/indodax`: Get indodax portfolio\n'
    s += '* `/indodax_add <PAIR> <BUY PRICE>`: Add pair to indodax portfolio\n'
    s += '* `/indodax_del <PAIR>`: Remove pair to indodax portfolio\n'
    s += '* `/help`: Show this\n'
    return {'text': s, 'parse_mode': 'MarkdownV2'}


def rss_add(user_id, chat_id, rss_url):
    # TODO: Premium user?
    premium_users = ['405179790']
    limit = 1
    count = db.session.query(RSSNotification.id).count()
    if count >= limit and user_id not in premium_users:
        return {'text': f'Sorry, currently we only allow max {limit} RSS URLs per user 🙏🏻'}
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


def rss_del(user_id: str, id: str) -> dict:
    notif = db.session.query(RSSNotification) \
        .filter(RSSNotification.user_id == user_id, RSSNotification.id == id) \
        .first()
    if notif:
        db.session.delete(notif)
        db.session.commit()
        reply = '✅ RSS notification deleted'
    else:
        reply = '⚠️ RSS notification not found'
    return {'text': reply, 'parse_mode': 'html'}


def trading_portfolio_add(user_id: str, chat_id: str, exchange: str, pair_id: str, buy_price: float) -> dict:
    portfolio = db.session.query(TradingPortfolio) \
        .filter(TradingPortfolio.user_id == user_id) \
        .first()
    new_data = {exchange: {pair_id: buy_price}}
    if not portfolio:
        portfolio = TradingPortfolio(user_id=user_id, chat_id=chat_id, data=new_data)
        db.session.add(portfolio)
    else:
        tmp = dict(portfolio.data)
        portfolio.data = helper.deep_update(tmp, new_data)
        portfolio.chat_id = chat_id
        flag_modified(portfolio, 'data')
    db.session.commit()
    reply = '✅ Portfolio updated'
    return {'text': reply, 'parse_mode': 'html'}


def trading_portfolio_del(user_id: str, chat_id: str, exchange: str, pair_id: str) -> dict:
    portfolio = db.session.query(TradingPortfolio) \
        .filter(TradingPortfolio.user_id == user_id) \
        .first()
    if portfolio and exchange in portfolio.data:
        portfolio.chat_id = chat_id
        tmp = dict(portfolio.data)
        tmp[exchange].pop(pair_id)
        portfolio.data = tmp
        flag_modified(portfolio, 'data')
        db.session.commit()
        reply = '✅ Pair removed'        
    else:
        reply = '⚠️ Pair not found'
    return {'text': reply, 'parse_mode': 'html'}

def indodax_summary(user_id: str) -> dict:
    portfolio = db.session.query(TradingPortfolio) \
        .filter(TradingPortfolio.user_id == user_id) \
        .first()
    if portfolio and 'indodax' in portfolio.data and portfolio.data['indodax']:
        reply = indodax.get_indodax_summary(portfolio.data['indodax'])
    else:
        reply = 'ℹ️ No portfolio found'
    return {'text': reply, 'parse_mode': 'html'}

def ssl_before_expired(chat_id: str, hostname: str) -> dict:
    try:
        num_days = ssl.get_num_days_before_expired(hostname)        
        icon = '🟢'
        if num_days <= 0:
            icon = '🔴'
        elif num_days <= 7:
            icon = '🟡'
        reply = f'{icon} {hostname} expires in {num_days} day(s)'
    except:
        reply = f'⚠️ Unable to get SSL information of {hostname}'
    return {'text': reply, 'parse_mode': 'html'}
