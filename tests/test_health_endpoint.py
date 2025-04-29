import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from src.db_factory.get_db import get_db
from src.main import app
from tests.mocked_db import override_get_db

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert "disk" in response.json()
    assert "db" in response.json()
    assert "ram" in response.json()
    assert "cpu" in response.json()
