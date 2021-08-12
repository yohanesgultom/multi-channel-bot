import utils.helper as helper
from channel.telegram.models import db, RSSNotification, TradingPortfolio
from utils.indodax import get_indodax_summary


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


def trading_portfolio_add(user_id: str, exchange: str, pair_id: str, buy_price: float) -> dict:
    portfolio = db.session.query(TradingPortfolio) \
        .filter(TradingPortfolio.user_id == user_id) \
        .first()
    new_data = {exchange: {pair_id: buy_price}}
    if not portfolio:
        portfolio = TradingPortfolio(user_id=user_id, data=new_data)
        db.session.add(portfolio)
    else:
        portfolio.data.update(new_data)
    db.session.commit()
    reply = '✅ Portfolio updated'
    return {'text': reply, 'parse_mode': 'html'}


def trading_portfolio_del(user_id: str, exchange: str, pair_id: str) -> dict:
    portfolio = db.session.query(TradingPortfolio) \
        .filter(TradingPortfolio.user_id == user_id) \
        .first()
    if portfolio and exchange in portfolio.data:
        tmp = portfolio.data[exchange]
        tmp.pop(pair_id)
        portfolio.data = tmp
        db.session.commit()
        reply = '✅ Pair removed'        
    else:
        reply = '⚠️ Pair not found'
    return {'text': reply, 'parse_mode': 'html'}

def indodax(user_id: str) -> dict:
    portfolio = db.session.query(TradingPortfolio) \
        .filter(TradingPortfolio.user_id == user_id) \
        .first()
    if portfolio and 'indodax' in portfolio.data:
        reply = get_indodax_summary(portfolio.data['indodax'])
    else:
        reply = 'ℹ️ No portfolio found'
    return {'text': reply, 'parse_mode': 'html'}
