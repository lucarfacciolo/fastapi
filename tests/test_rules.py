import datetime as dt
from src.services.apply_rules import apply_rules_to_company


def rule_set():
    return [
        {
            "input": "total_employees",
            "feature_name": "head_count_feature",
            "operation": {"greater_than": 80},
            "match": 0,
            "default": 1,
        },
        {
            "input": "company_age",
            "feature_name": "age_feature",
            "operation": {"less_than": 10},
            "match": 1,
            "default": 0,
        },
        {
            "input": "is_usa_based",
            "feature_name": "usa_based_feature",
            "operation": {"equal": True},
            "match": 1,
            "default": 0,
        },
        {
            "input": "is_saas",
            "feature_name": "is_saas_feature",
            "operation": {"equal": True},
            "match": 1,
            "default": 0,
        },
    ]


def test_apply_rules():
    mock_company = {
        "id": 2,
        "company_name": "Test",
        "url": "test.com",
        "founded_year": "2020",
        "total_employees": "1000",
        "headquarters_city": "Sao Paulo",
        "employee_locations": {"Sao Paulo": "10"},
        "employee_growth_2y": "10",
        "employee_growth_1y": "20",
        "employee_growth_6m": "20",
        "description": "Test company",
        "industry": "Test company",
        "imported_at": dt.datetime.utcnow(),
    }
    rules = rule_set()
    features = apply_rules_to_company(mock_company, rules)
    assert features == {
        "head_count_feature": 0,
        "age_feature": 0,
        "usa_based_feature": 0,
        "is_saas_feature": 1,
    }
