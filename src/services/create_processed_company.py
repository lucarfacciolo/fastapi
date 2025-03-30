from datetime import datetime
from src.models.db.processed_company import ProcessedCompany


def create_processed_company(url: str, last_processed: datetime, features: dict):
    return ProcessedCompany(
        url=url, processed_features=features, last_processed=last_processed
    )
