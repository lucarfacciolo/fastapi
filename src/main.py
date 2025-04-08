from fastapi import FastAPI, File, Depends, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import Table, MetaData
import logging
from datetime import datetime
from typing import List

from src.db_factory.get_db import get_db
from src.constants.file_extension import FileExtension
from src.helpers.parsers import parse_csv, parse_json
from src.services.init_logging import init_logging
import src.helpers.health_helpers as hhelper
from src.models.request_models.process_company_request_model import (
    ProcessCompanyRequestModel,
)
from src.models.return_models.get_company_return_model import GetCompanyReturnModel
from src.models.return_models.health_return_model import HealthReturnModel
from src.db_factory.db_factory import engine
from src.services.apply_rules import apply_rules_to_company
from src.services.create_processed_company import create_processed_company
from src.services.get_imported_data import get_imported_data

init_logging()
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post(
    "/import_company_data",
    response_description="Return how many records were imported",
    tags=["Companies"],
)
async def import_company_data(
    file: UploadFile = File(...), db: Session = Depends(get_db)
) -> JSONResponse:
    logger.info("import_company_data endpoint hit")

    f_ext = file.filename.split(".")[-1].lower()  # type:ignore
    try:
        file_extension = FileExtension(f_ext)
        if file_extension == FileExtension.CSV:
            companies = parse_csv(file)
        elif file_extension == FileExtension.JSON:
            companies = parse_json(file)

        db.add_all(companies)
        db.commit()
        logger.info(f"{len(companies)} companies imported successfully")
        return JSONResponse(content=f"{len(companies)} were imported.", status_code=200)
    except Exception as e:
        logger.exception("Exception while importing company data")
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")


@app.post(
    "/process_company",
    response_description="Process companies using a rule set",
    tags=["Companies"],
)
async def process_company(
    request: ProcessCompanyRequestModel, db: Session = Depends(get_db)
) -> JSONResponse:
    logger.info("process_company endpoint hit")
    try:
        urls = request.urls
        rules = request.rule_set

        company_table = Table(
            "companies", MetaData(), autoload_with=engine, extend_existing=True
        )
        companies = db.query(company_table).filter(company_table.c.url.in_(urls)).all()

        last_processed = datetime.utcnow()
        features = []
        processed_companies = []

        for c in companies:
            feature = apply_rules_to_company(c, rules)
            features.append(feature)
            processed_companies.append(
                create_processed_company(c.url, last_processed, feature)
            )

        db.add_all(processed_companies)
        db.commit()
        logger.info(f"Processed {len(features)} companies successfully")
        return JSONResponse(content=features, status_code=200)
    except Exception as e:
        logger.exception("Exception while processing company data")
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")


@app.get(
    "/get_companies",
    response_model=List[GetCompanyReturnModel],
    tags=["Companies"],
)
async def get_companies(db: Session = Depends(get_db)) -> JSONResponse:
    logger.info("get_companies endpoint hit")
    try:
        p_company_table = Table(
            "processed_companies",
            MetaData(),
            autoload_with=engine,
            extend_existing=True,
        )
        companies_table = Table(
            "companies", MetaData(), autoload_with=engine, extend_existing=True
        )

        processed = db.query(p_company_table).all()
        urls = [c.url for c in processed]
        originals = (
            db.query(companies_table).filter(companies_table.c.url.in_(urls)).all()
        )

        response_list = []
        for p in processed:
            company = next((c for c in originals if c.url == p.url), None)
            if not company:
                logger.exception(f"company {p.url} not found in processed companies")
                continue

            response_list.append(
                {
                    "url": p.url,
                    "imported_data": get_imported_data(company),
                    "processed_features": p.processed_features,
                    "date_imported": str(company.imported_at),
                    "last_processed": str(p.last_processed),
                }
            )

        logger.info(f"Returned {len(response_list)} processed companies")
        return JSONResponse(content=response_list, status_code=200)
    except Exception as e:
        logger.exception("Exception while fetching companies")
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")


@app.get(
    "/health",
    response_model=HealthReturnModel,
    tags=["Health"],
)
async def health():
    logger.info("health endpoint hit")
    try:

        return_json = {
            "disk": hhelper.check_disk(),
            "db": hhelper.check_db(),
            "ram": hhelper.check_ram(),
            "cpu": hhelper.check_cpu(),
        }

        logger.info("Health check completed successfully")
        return JSONResponse(status_code=200, content=return_json)
    except Exception as e:
        logger.exception("Exception during health check")
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")
