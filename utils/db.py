import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLLITE_DB_URL = 'sqlite:///db.sqlite3'
DB_URL = settings.env('DB_URL', default=SQLLITE_DB_URL)

def init_db():
    engine = create_engine(DB_URL)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    Base = declarative_base()
    return engine, session, Base

def create_all(base, engine):
    base.metadata.create_all(engine)

engine, session, Base = init_db()