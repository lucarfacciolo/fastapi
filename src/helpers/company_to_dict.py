from src.models.db.company import Company


def companies_to_dict(companies: list[Company]) -> list[dict]:
    return [
        {key: value for key, value in vars(company).items() if not key.startswith("_")}
        for company in companies
    ]
