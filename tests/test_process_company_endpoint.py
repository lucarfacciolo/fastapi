import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from src.db_factory.get_db import get_db
from src.main import app
from tests.mocked_db import override_get_db, override_mocked_url


def test_matched_company():
    app.dependency_overrides[get_db] = override_mocked_url
    client = TestClient(app, raise_server_exceptions=True)
    with open("files/test_process_companies.json") as f:
        json_data = json.load(f)

    response = client.post("/process_company", json=json_data)

    assert response.status_code == 200
    assert len(response.json()) == 1

    keys = response.json()[0].keys()
    assert "head_count_feature" in keys
    assert "age_feature" in keys
    assert "usa_based_feature" in keys
    assert "is_saas_feature" in keys
    app.dependency_overrides.clear()


def test_no_match():
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app, raise_server_exceptions=True)
    with open("files/process_companies.json") as f:
        json_data = json.load(f)

    response = client.post("/process_company", json=json_data)

    assert response.status_code == 200
    assert len(response.json()) == 0
    app.dependency_overrides.clear()
