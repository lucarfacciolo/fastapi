from pydantic import BaseModel
from typing import List, Dict, Union


class Operation(BaseModel):
    greater_than: Union[int, None] = None
    less_than: Union[int, None] = None
    equal: Union[bool, None] = None


class Rule(BaseModel):
    input: str
    feature_name: str
    operation: Operation
    match: int
    default: int


class ProcessCompanyRequestModel(BaseModel):
    urls: List[str]
    rule_set: List[Rule]
