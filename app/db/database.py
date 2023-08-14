import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import settings

DATABASE_USERNAME = settings.DATABASE_USERNAME
DATABASE_PASSWORD = settings.DATABASE_PASSWORD
DATABASE_HOST = settings.DATABASE_HOST
DATABASE_NAME = settings.DATABASE_NAME

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    # Independent database session for each request
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
