# external
from fastapi import FastAPI, File, Depends, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import Table, MetaData
import logging
from datetime import datetime

# internal
from src.db_factory.get_db import get_db
from src.constants.file_extension import FileExtension
from src.helpers.parsers import parse_csv, parse_json
from src.services.init_logging import init_logging
import src.helpers.health_helpers as hhelper
from src.models.process_company_request_model import ProcessCompanyRequestModel
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
    description="""
          Upload a file with the following structure:

          
          company_name: str
          url: str
          founded_year: int
          total_employees: int
          headquarters_city: str
          employee_locations: json
          employee_growth_2y: float
          employee_growth_1y: float
          employee_growth_6m: float
          description: str
          industry: str  
          """,
)
async def import_company_data(
    file: UploadFile = File(...), db: Session = Depends(get_db)
) -> JSONResponse:

    logger.info(f"request was made. File {file} was sent")
    if not file:
        logger.exception("no file was uploaded")
        raise HTTPException(status_code=500, detail="No file was uploaded")

    f_ext = file.filename.split(".")[-1].lower()  # type:ignore
    try:
        file_extension = FileExtension(f_ext)
        if file_extension == FileExtension.CSV:
            logger.info("csv file being parsed")
            companies = parse_csv(file)
        elif file_extension == FileExtension.JSON:
            logger.info("json file being parsed")
            companies = parse_json(file)

        logger.info("file parsed successfully")
        logger.info("attempt to import companies")

        db.add_all(companies)
        db.commit()
        logger.info("import company data finished gracefully")
        return JSONResponse(
            content=f"{len(companies)} were imported.",
            status_code=200,
        )
    except Exception as e:
        logger.exception(f"error on saving company data {e}")
        raise HTTPException(status_code=500, detail=f"Bad Request {e}")


@app.post(
    "/process_company",
    description="receives a json with a list of urls and a json rule set. Process already in db companies given rule set",
    response_description="returns a json array containing the processing output of each url(company) sent",
)
async def process_company(
    request: ProcessCompanyRequestModel, db: Session = Depends(get_db)
) -> JSONResponse:
    logger.info("process company request was made")
    try:
        urls = request.urls
        rules = request.rule_set

        companyTable = Table(
            "companies", MetaData(), autoload_with=engine, extend_existing=True
        )
        logger.info("getting companies")
        companies = db.query(companyTable).filter(companyTable.c.url.in_(urls)).all()
        logger.info("companies retrieved")
        last_processed = datetime.utcnow()
        features = []
        processed_companies = []
        logger.info("processing features")
        for c in companies:
            # c.last_processed = last_processed
            feature = apply_rules_to_company(c, rules)
            features.append(feature)
            processed_companies.append(
                create_processed_company(c.url, last_processed, feature)
            )
        logger.info("features processed")
        logger.info("saving into db")
        db.add_all(processed_companies)
        db.commit()
        logger.info("process company finished gracefully")
        return JSONResponse(content=features, status_code=200)
    except Exception as e:
        logger.exception(f"error processing companies {e}")
        raise HTTPException(status_code=500, detail=f"Bad Request {e}")


@app.get(
    "/get_companies",
    description="""
          list only previously processed companies, in a json array with the following format:


          url: str
          imported_data:json
          processed_features:json
          date_imported: str(datetime) in utc
          last_processed: str(datetime) in utc
          """,
)
async def get_companies(db: Session = Depends(get_db)) -> JSONResponse:
    logger.info("get companies was requested")
    try:
        p_companies = Table(
            "processed_companies",
            MetaData(),
            autoload_with=engine,
            extend_existing=True,
        )
        p_companies = db.query(p_companies).all()
        urls = [c.url for c in p_companies]
        companies = Table(
            "companies", MetaData(), autoload_with=engine, extend_existing=True
        )
        companies = db.query(companies).filter(companies.c.url.in_(urls)).all()
        responses = []
        for p_company in p_companies:
            company = [
                company for company in companies if company.url == p_company.url
            ][0]

            response = dict(
                url=p_company.url,
                imported_data=get_imported_data(company),
                processed_features=p_company.processed_features,
                date_imported=str(company.imported_at),
                last_processed=str(p_company.last_processed),
            )
            responses.append(response)
        logger.info("get companies finished gracefully")
        return JSONResponse(content=responses, status_code=200)
    except Exception as e:
        logger.exception(f"error getting companies {e}")
        raise HTTPException(status_code=500, detail=f"Bad Request {e}")


@app.get(
    "/health",
    description="check api, db, ram and cpu statuses",
    response_description="returns json with main statuses",
)
async def health():
    logger.info("health request was made")
    try:
        disk = hhelper.check_disk()
        db = hhelper.check_db()
        ram = hhelper.check_ram()
        cpu = hhelper.check_cpu()
        return_json = dict(disk=disk, db=db, ram=ram, cpu=cpu)
        logger.info("health finished gracefully")
        return JSONResponse(status_code=200, content=return_json)
    except Exception as e:
        logger.exception(f"error on health request {e}")
        raise HTTPException(status_code=500, detail=f"Bad Request {e}")
