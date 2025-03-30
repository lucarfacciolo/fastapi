# external
from sqlalchemy import Column, String, JSON, DateTime, Integer

# internal
from src.db_factory.db_factory import Base


class ProcessedCompany(Base):  # type:ignore
    __tablename__ = "processed_companies"
    # (NOTE lfacciolo) will keep everything nullable and string to simplify treatments
    # (NOTE lfacciolo) this should have a foreign key
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=True)
    processed_features = Column(
        JSON, nullable=True
    )  # (NOTE lfacciolo) will keep this json to process unseen features
    last_processed = Column(DateTime, nullable=False)
