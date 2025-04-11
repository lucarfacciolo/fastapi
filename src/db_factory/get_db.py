# external
from typing import Generator

from sqlalchemy.orm import Session, sessionmaker

# internal
from src.db_factory.db_factory import SessionLocal


# Singleton instance
class DatabaseInstance:
    _instance = None

    def __new__(cls) -> sessionmaker[Session]:
        if cls._instance is None:
            cls._instance = SessionLocal()
        return cls._instance  # type:ignore


def get_db() -> Generator[DatabaseInstance, None, None]:
    db = DatabaseInstance()
    try:
        yield db  # type:ignore
    finally:
        pass  # Singleton session, do not close
