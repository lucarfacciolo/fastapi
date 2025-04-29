import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from src.db_factory.get_db import get_db
from src.main import app
from tests.mocked_db import override_get_db

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_data_json():
    with open("files/company-dataset.json", "rb") as f:
        response = client.post(
            "/import_company_data",
            files={"file": ("test_companies.json", f, "application/json")},
        )
    assert response.status_code == 200


def test_data_csv():
    with open("files/company-dataset.csv", "rb") as f:
        response = client.post(
            "/import_company_data",
            files={"file": ("test_companies.csv", f, "text/csv")},
        )
    assert response.status_code == 200


def test_data_other_file_extension():
    files = {"file": ("test.txt", "", "application/json")}
    response = client.post("/import_company_data", files=files)
    assert response.status_code == 500


def test_wrong_data():
    # NOTE(lfacciolo) should not break, only ignore new columns
    with open("files/test_wrong_data.csv", "rb") as f:
        response = client.post(
            "/import_company_data",
            files={"file": ("test_companies.csv", f, "text/csv")},
        )
    assert response.status_code == 200
