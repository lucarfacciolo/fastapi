from db_factory.db_factory import Base, engine

Base.metadata.create_all(bind=engine)
