import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime
from src.models.db.company import Company
from src.models.db.processed_company import ProcessedCompany
from unittest.mock import MagicMock


class MockDBSession:
    def __init__(self, expected_urls):
        self.added = []
        self.committed = False
        self.expected_urls = expected_urls or []

        # 👇 Create a mock for query().filter().all()
        self.mock_companies = [
            Company(
                id=1,
                company_name="TestCorp",
                url="https://test.com",
                founded_year="2020",
                total_employees="100",
                headquarters_city="New York",
                employee_locations={"USA": 100},
                employee_growth_2y="0.1",
                employee_growth_1y="0.05",
                employee_growth_6m="0.02",
                description="A SaaS company providing solutions.",
                industry="Software",
                imported_at="2024-01-01",
            )
        ]

        self.mock_processed_companies = [
            ProcessedCompany(
                id=1,
                url="https://test.com",
                processed_features={
                    "head_count_feature": 0,
                    "age_feature": 1,
                    "usa_based_feature": 1,
                    "is_saas_feature": 1,
                },
                last_processed=datetime(2024, 3, 1),
            )
        ]

        self.query_mock = MagicMock()
        self.query_mock.filter.return_value.all.return_value = self.mock_companies

    def add_all(self, records):
        self.added.extend(records)

    def commit(self):
        self.committed = True

    def query(self, model):
        class DummyQuery:
            def __init__(self, mock_companies, expected_urls, mock_processed_companies):
                self.mock_companies = mock_companies
                self.expected_urls = expected_urls
                self.mock_processed_companies = mock_processed_companies
                self.model = model

            def filter(self, _):
                return self

            def all(self):
                if self.model.name == "companies":
                    return [
                        c for c in self.mock_companies if c.url in self.expected_urls
                    ]
                else:
                    return [
                        c
                        for c in self.mock_processed_companies
                        if c.url in self.expected_urls
                    ]

        return DummyQuery(
            self.mock_companies, self.expected_urls, self.mock_processed_companies
        )


# Override FastAPI dependency
def override_get_db():
    db = MockDBSession(expected_urls=[])
    yield db


def override_mocked_url():
    db = MockDBSession(expected_urls=["https://test.com"])
    yield db
