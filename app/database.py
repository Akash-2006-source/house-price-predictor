from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
class Base(DeclarativeBase): pass
def init_db(app):
    engine = create_engine(app.config['DATABASE_URL'], pool_pre_ping=True)
    app.extensions['db_engine'] = engine
    app.extensions['db_session'] = sessionmaker(bind=engine, expire_on_commit=False)
    from .models import Prediction
    Base.metadata.create_all(engine)
def session(): return current_app.extensions['db_session']()
