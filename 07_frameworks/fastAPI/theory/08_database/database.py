"""
Centralizes the database connection setup. Every other file that
needs to talk to the database imports from here -- never duplicate
this setup elsewhere.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite connection string: a single file named app.db in this folder.
# `check_same_thread=False` is a SQLite-specific quirk needed because
# FastAPI may use the same session across different threads.
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal is a FACTORY for creating new sessions -- it doesn't
# create a session itself, it creates the "recipe" for making one.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class every ORM model inherits from. SQLAlchemy
# uses it to keep track of every table you've defined.
Base = declarative_base()


def get_db():
    """
    Dependency (see topic 6) that provides a database session to an
    endpoint, and guarantees it gets closed afterward.

    The `yield` (instead of `return`) is what makes this special:
    code BEFORE yield runs before the endpoint, code AFTER yield runs
    after the endpoint finishes -- even if it raised an exception.
    This is the standard pattern for any resource that needs cleanup.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
