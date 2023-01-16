from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api.db.config import Settings

SQLALCHEMY_DATABASE_URL = "postgresql://postgres_api:postgres_api@db/postgres_api"

engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()

# DB dependency


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
