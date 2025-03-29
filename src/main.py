from fastapi import FastAPI, File, Depends, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import logging
import os

from src.db_factory.get_db import get_db
from src.services.check_city_location import city_in_usa
from src.constants.file_extension import FileExtension
from src.helpers.parsers import parse_csv, parse_json


log_folder = os.path.join(os.path.dirname(__file__), "../logs")
log_file = os.path.join(log_folder, "app.log")
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post(
    "/import_company_data",
    description="Given a json or csv of companies, saves and returns records imported",
    response_description="Return how many records were imported",
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
        logger.info("attempt to save companies")

        db.add_all(companies)
        db.commit()
        logger.info("companies saved")
        return JSONResponse(
            content=f"{len(companies)} were imported.",
            status_code=200,
        )
    except Exception as e:
        logger.exception(f"bad request on saving company data {e}")
        raise HTTPException(status_code=500, detail="Bad Request")
