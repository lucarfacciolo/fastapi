from db_factory.db_factory import engine, Base
from models.db_models.company import Company

Base.metadata.create_all(bind=engine)
