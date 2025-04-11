from db_factory.db_factory import Base, engine
from models.db.company import Company
from models.db.processed_company import ProcessedCompany

Base.metadata.create_all(bind=engine)
