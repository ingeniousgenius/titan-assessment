import os

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from util import SingletonMeta
from settings import DATABASE_URL

class DBSession(metaclass=SingletonMeta):
    """Singleton wrapper around a SQLAlchemy session instance."""

    def __init__(self):
        # Initialized exactly once per process by the SingletonMeta.
        engine = create_engine(DATABASE_URL)
        session = scoped_session(sessionmaker(bind=engine))
        self.session = session

def get_session():
    """Get the singleton SQLAlchemy session instance."""
    return DBSession().session

def setup_database(app: Flask) -> None:
    @app.teardown_appcontext
    def shutdown_session(exception=None) -> None: # type: ignore[misc]
        get_session().remove()

session = get_session()