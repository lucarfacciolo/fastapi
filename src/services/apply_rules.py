from src.helpers.company_age import get_company_age
from src.models.request_models.process_company_request_model import Rule
from src.services.check_city_location import city_in_usa
from typing import List


def apply_rules_to_company(company, rules: List[Rule]) -> dict:
    features = {}

    for rule in rules:
        input_value = getattr(company, rule.input, None)

        if rule.operation.greater_than is not None:
            if (
                input_value is not None
                and float(input_value) > rule.operation.greater_than
            ):
                features[rule.feature_name] = rule.match
            else:
                features[rule.feature_name] = rule.default

        elif rule.operation.less_than is not None:
            if (
                input_value is not None
                and float(input_value) < rule.operation.less_than
            ):
                features[rule.feature_name] = rule.match
            else:
                features[rule.feature_name] = rule.default

        elif rule.operation.equal is not None:
            if input_value is not None and input_value == rule.operation.equal:
                features[rule.feature_name] = rule.match
            else:
                features[rule.feature_name] = rule.default

    return features


def apply_new_rules_to_company(company: dict, rules: dict) -> dict:
    company["is_usa_based"] = city_in_usa(company["headquarters_city"])
    company["is_saas"] = True
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
