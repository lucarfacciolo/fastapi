# external
import psutil
from sqlalchemy import text
import logging


# internal
from src.db_factory.get_db import SessionLocal


logger = logging.getLogger(__name__)


def check_disk() -> str:
    try:
        return str(psutil.disk_usage("/").percent) + "%"
    except Exception as e:
        logging.exception(f"couldn't check disk {e}")
        return f"{e}"


def check_ram() -> str:
    try:
        return str(psutil.virtual_memory().percent) + "%"
    except Exception as e:
        logging.exception(f"couldn't check ram {e}")
        return f"{e}"


def check_cpu() -> str:
    try:
        return str(psutil.cpu_percent()) + "%"
    except Exception as e:
        logging.exception(f"couldn't check cpu {e}")
        return f"{e}"


def check_db() -> bool:
    try:
        conn = SessionLocal()
        conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logging.exception(f"couldn't check db {e}")
        return False
