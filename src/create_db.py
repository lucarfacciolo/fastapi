# internal
from db_factory.db_factory import engine, Base
from models.company import Company  # needs to import in order to create
from models.processed_company import ProcessedCompany

Base.metadata.create_all(bind=engine)
