# external
from pydantic import BaseModel


class HealthReturnModel(BaseModel):  # type:ignore
    api: str
    disk: str
    db: bool
    ram: str
    cpu: str
