from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime
from pydantic import BaseModel
from db_factory.db_factory import Base
from pydantic import Field
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime


class Company(Base):  # type:ignore
    __tablename__ = "companies"
    # (NOTE lfacciolo) will keep everything nullable and string to simplify treatments
    id = Column(Integer, primary_key=True)
    company_name = Column(String, nullable=True)
    url = Column(String, nullable=True)
    founded_year = Column(String, nullable=True)
    total_employees = Column(String, nullable=True)
    headquarters_city = Column(String, nullable=True)
    employee_locations = Column(JSON, nullable=True)
    employee_growth_2y = Column(String, nullable=True)
    employee_growth_1y = Column(String, nullable=True)
    employee_growth_6m = Column(String, nullable=True)
    description = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    imported_at = Column(DateTime, nullable=True)  # utc always
    last_processed = Column(DateTime, nullable=True)  # utc always
    company_age = Column(
        String, nullable=True
    )  # (NOTE lfacciolo) saving this here is not a good idea
    is_usa_based = Column(Boolean, nullable=True)
    is_saas = Column(Boolean, nullable=True)
