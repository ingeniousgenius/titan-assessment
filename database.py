import os

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from util import SingletonMeta

DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'catalogue')

if not DB_USER or not DB_HOST or not DB_PORT or not DB_PASS:
    raise Exception("The database credentials are missing from the environment")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}"

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