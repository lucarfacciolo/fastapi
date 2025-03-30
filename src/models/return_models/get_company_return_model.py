# external
from pydantic import BaseModel, Json


class GetCompanyReturnModel(BaseModel):  # type:ignore
    url: str
    imported_data: Json
    processed_features: Json
    date_imported: str
    last_processed: str
