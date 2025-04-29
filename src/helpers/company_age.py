from datetime import datetime


def get_company_age(age: str) -> str:
    year_founded = int(age)
    years = datetime.utcnow().year - year_founded
    return str(years)
