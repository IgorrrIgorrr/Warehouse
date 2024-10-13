# test_main.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from warehouse.models import Base 
from warehouse.database import get_db
from warehouse.main import app


DSN = "sqlite:///./test.db"
engine = create_engine(DSN)

test_session = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def test_db():
    db = test_session()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_product(client):
    product_data = {
        "name": "Test Product",
        "description": "A product for testing",
        "price": 100.0,
        "stock": 10
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]
    assert data["stock"] == product_data["stock"]

def test_get_products(client):
    response = client.get("/products")
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    assert len(products) > 0

def test_get_product_by_id(client):
    product_id = 1  
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    product = response.json()
    assert product["id"] == product_id

def test_update_product(client):
    product_update_data = {
        "name": "Updated Product",
        "description": "Updated description",
        "price": 150.0,
        "stock": 20
    }
    product_id = 1  
    response = client.put(f"/products/{product_id}", json=product_update_data)
    assert response.status_code == 200
    updated_product = response.json()
    assert updated_product["name"] == product_update_data["name"]

def test_delete_product(client):
    product_id = 1  # Подставьте корректный ID продукта
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Product deleted successfully"
