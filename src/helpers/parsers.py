import csv
from datetime import datetime
from fastapi import HTTPException, UploadFile
from io import StringIO
import json
import logging
from src.models.db.company import Company
from typing import List

logger = logging.getLogger(__name__)


def parse_csv(file: UploadFile) -> List[Company]:
    logger.info("csv file being parsed")
    try:
        contents = file.file.read().decode("utf-8")
        csv_reader = csv.DictReader(StringIO(contents))
        rows = list(csv_reader)
        companies = _parse_data(rows)
        return companies
    except Exception as e:
        logger.exception(f"error parsing csv{e}")
        raise HTTPException(status_code=400, detail=f"Error reading CSV file: {str(e)}")


def _parse_data(data: List[dict], is_json=False) -> List[Company]:
    companies = []
    imported_at = datetime.utcnow()
    for d in data:
        try:
            company = Company(
                company_name=d.get("company_name"),
                url=d.get("url"),
                founded_year=d.get("founded_year"),
                total_employees=d.get("total_employees"),
                headquarters_city=d.get("headquarters_city"),
                employee_locations=(
                    d.get("employee_locations")
                    if is_json
                    else json.loads(d.get("employee_locations"))  # type:ignore
                ),
                employee_growth_2y=d.get("employee_rowth_2Y"),
                employee_growth_1y=d.get("employee_growth_1Y"),
                employee_growth_6m=d.get("employee_growth_6M"),
                description=d.get("description"),
                industry=d.get("industry"),
                imported_at=imported_at,
            )
            companies.append(company)
        except Exception as e:
            logger.exception(f"error parsing {d} -> {e}")
            raise e
    return companies


def parse_json(file: UploadFile) -> List[Company]:
    logger.info("json file being parsed")
    try:
        contents = file.file.read().decode("utf-8")
        json_data = json.loads(contents)
        companies = _parse_data(json_data, is_json=True)
        return companies
    except Exception as e:
        logger.exception(f"error parsing json{e}")
        raise HTTPException(
            status_code=400, detail=f"Error reading JSON file: {str(e)}"
        )
