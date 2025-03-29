import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session, DeclarativeBase

# Ensure the "db" folder exists
os.makedirs("db", exist_ok=True)

DATABASE_URL: str = "sqlite:///./db/database.db"

engine: Engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base: DeclarativeBase = declarative_base()
