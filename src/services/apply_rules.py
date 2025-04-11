from typing import List

from src.models.request_models.process_company_request_model import Rule


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
