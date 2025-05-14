from src.helpers.company_age import get_company_age
from src.helpers.predict_saas import predict_saas

# from src.models.request_models.process_company_request_model import Rule
from src.services.check_city_location import city_in_usa


def apply_rules_to_company(company: dict, rules: dict) -> dict:
    company["is_usa_based"] = city_in_usa(company["headquarters_city"])
    company["is_saas"] = predict_saas(company["description"], threshold=0)
    company["company_age"] = get_company_age(company["founded_year"])
    features = {}

    for rule in rules:
        var = rule["input"]
        value = int(company[var])
        operation_type_value = rule["operation"]
        output = None
        for key in operation_type_value.keys():
            reference_val = operation_type_value[key]
            if key == "greater_than":
                output = rule["match"] if value > reference_val else rule["default"]
                break
            elif key == "lower_than":
                output = rule["match"] if value < reference_val else rule["default"]
                break
            else:
                output = rule["match"] if value == reference_val else rule["default"]
                break
        features[rule["feature_name"]] = output
    return features
