import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from src.db_factory.get_db import get_db
from src.main import app
from tests.mocked_db import override_get_db, override_mocked_url


def test_get_no_processed_companies():
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    response = client.get("/get_companies")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0
    app.dependency_overrides.clear()


def test_get_companies():
    app.dependency_overrides[get_db] = override_mocked_url
    client = TestClient(app)
    response = client.get("/get_companies")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    data = response.json()[0]
    assert "url" in data
    assert "imported_data" in data
    assert "processed_features" in data
    assert "date_imported" in data
    assert "last_processed" in data
    assert isinstance(data["url"], str)
    assert isinstance(data["imported_data"], dict)
    assert isinstance(data["processed_features"], dict)
    assert isinstance(data["date_imported"], str)
    assert isinstance(data["last_processed"], str)
    imported = data["imported_data"]
    expected_imported_keys = {
        "company_name",
        "url",
        "founded_year",
        "total_employees",
        "headquarters_city",
        "employee_locations",
        "employee_growth_2y",
        "employee_growth_1y",
        "employee_growth_6m",
        "description",
        "industry",
    }
    assert set(imported.keys()) == expected_imported_keys
    assert isinstance(imported["employee_locations"], dict)
    app.dependency_overrides.clear()
