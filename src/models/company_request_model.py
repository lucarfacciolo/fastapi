# external
from pydantic import BaseModel


class CompanyRequestModel(BaseModel):  # type:ignore
    id: str
    company_name: str
    url: str
    founded_year: str
    total_employees: str
    headquarters_city: str
    employee_locations: str
    employee_growth_2y: str
    employee_growth_1y: str
    employee_growth_6m: str
    description: str
    industry: str
