import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

#Úplně jsem nevěděl, co mám v této aplikaci testovat, tenhle typ testů bych standardně napsal v Postman

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from Kucharka!"}

def test_get_recipes():
    response = client.get("/recipes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)