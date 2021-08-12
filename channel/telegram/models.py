from datetime import timezone
from sqlalchemy import TypeDecorator, Column, Integer, String, Text, JSON, TIMESTAMP
from sqlalchemy.orm.attributes import flag_modified
import utils.db as db


class TimeStamp(TypeDecorator):
    """
    Add tzinfo if not available
    Assuming the column always use UTC timezone
    """
    impl = TIMESTAMP(timezone=True)

    def process_result_value(self, value, dialect):
        if value and not value.tzinfo:
            value = value.replace(tzinfo=timezone.utc)
        return value


class RSSNotification(db.Base):
    __tablename__ = 'rss_notifications'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    chat_id = Column(String)
    rss_url = Column(Text, nullable=False)
    last_item_date = Column(TimeStamp)


class TradingPortfolio(db.Base):
    __tablename__ = 'trading_portfolios'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    chat_id = Column(String)
    data = Column(JSON, nullable=True)


db.create_all(db.Base, db.engine)
