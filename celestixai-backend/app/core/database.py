import time
from sqlalchemy.exc import OperationalError
from app.core.config import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(DATABASE_URL, pool_timeout=90)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    retries = 10
    delay = 3  # seconds
    for _ in range(retries):
        try:
            db = SessionLocal()
            yield db
            return
        except OperationalError:
            print("Database connection not available. Retrying...")
            time.sleep(delay)
    raise OperationalError("Failed to connect to database after {} retries".format(retries))
