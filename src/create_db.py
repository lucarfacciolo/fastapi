# internal
from db_factory.db_factory import engine, Base
from models.db.company import Company  # needs to import in order to create
from models.db.processed_company import ProcessedCompany

Base.metadata.create_all(bind=engine)
