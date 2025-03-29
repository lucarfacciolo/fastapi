from typing import Generator
from src.db_factory.db_factory import SessionLocal
from sqlalchemy.orm import sessionmaker, Session

#Singleton instance
class DatabaseInstance:
    _instance = None

    def __new__(cls) -> sessionmaker[Session]:
        if cls._instance is None:
            cls._instance = SessionLocal()
        return cls._instance

def get_db() -> Generator[DatabaseInstance,None,None]:
    db = DatabaseInstance()
    try:
        yield db
    finally:
        pass  # Singleton session, do not close