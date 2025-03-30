# external
from pydantic import BaseModel, Json


class HealthReturnModel(BaseModel):  # type:ignore
    api: str
    disk: str
    db: bool
    ram: str
    cpu: str
