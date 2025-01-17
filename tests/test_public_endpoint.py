import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import app
from database.models import User
from dotenv import load_dotenv

# Load environment variables before the test
load_dotenv()
import os


# Fixture to set up the FastAPI test client
@pytest.fixture(scope="module")
def client():
    client = TestClient(app)
    yield client


@pytest.mark.asyncio
def test_signup_with_real_db(client):
    # Define test user data
    test_data = {
        "email": "testuser@example.com",
        "password": "securepassword123"
    }

    # Send a POST request to the signup endpoint
    response = client.post("/public/signup", json=test_data)
    assert response.status_code == 200

@pytest.mark.asyncio
def test_login_with_real_db(client):
    test_data = {
        "email": "testuser@example.com",
        "password": "securepassword123"
    }

    # Send a POST request to the signup endpoint
    response = client.post("/public/login", json=test_data)
    assert response.status_code == 200
