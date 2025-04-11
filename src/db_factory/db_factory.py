import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, declarative_base, sessionmaker

DATABASE_URL: str = "sqlite:///db/database.db"
# Ensure the "db" folder exists
os.makedirs("db", exist_ok=True)


engine: Engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base: DeclarativeBase = declarative_base()
