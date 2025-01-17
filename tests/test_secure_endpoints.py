import os

import pytest
from fastapi.testclient import TestClient
from app import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.mark.asyncio
def test_get_fund_family_houses(client):
    headers = {"Authorization": os.getenv("MOCK_AUTH_TOKEN")}
    response = client.get("/secure/fund-family-houses", headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
def test_get_schemas_fund_family(client):
    headers = {"Authorization": os.getenv("MOCK_AUTH_TOKEN")}
    params = {"fund_family_name": "Bajaj Finserv Mutual Fund"}
    response = client.get("/secure/schemas-fund-family", headers=headers, params=params)
    print("STDOUT:", flush=True)
    print(dict(response.json()), flush=True)
    print("STDOUT:", flush=True)
    assert response.status_code == 200


@pytest.mark.asyncio
def test_acquire_mutual_funds_units(client):
    headers = {"Authorization": os.getenv("MOCK_AUTH_TOKEN")}
    purchase_data = {
        "ISIN": "INF209K01090",
        "no_of_units": 2000,
    }

    response = client.post("/secure/buy-funds", headers=headers, json=purchase_data)
    print("STDOUT:", flush=True)
    print(response.json(), flush=True)
    print("STDOUT:", flush=True)
    assert response.status_code == 200
