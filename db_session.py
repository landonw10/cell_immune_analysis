from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Connect to your existing SQLite DB
engine = create_engine("sqlite:///database.db", connect_args={"check_same_thread": False})

# Called to create a session for running queries
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

# Sets up engine, connecting to SQLite database
def init_db():
    # Creates tables if they don't already exist
    Base.metadata.create_all(bind=engine)