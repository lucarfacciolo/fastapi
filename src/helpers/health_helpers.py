import psutil
from sqlalchemy import text
import logging

from src.db_factory.get_db import SessionLocal


logger = logging.getLogger(__name__)


def check_disk() -> str:
    return str(psutil.disk_usage("/").percent) + "%"


def check_ram() -> str:
    return str(psutil.virtual_memory().percent) + "%"


def check_cpu() -> str:
    return str(psutil.cpu_percent()) + "%"


def check_db() -> str:
    try:
        conn = SessionLocal()
        conn.execute(text("SELECT 1"))
        return "Online"
    except Exception as e:
        return "Offline"
