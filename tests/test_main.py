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


@pytest.fixture(scope="module")
def setup_products(client):
    product = {"name": "Product 4", "description": "Test product", "price": 10.0, "stock": 100}
    response = client.post("/products", json=product)
    assert response.status_code == 200
    print("--------------------", response.json()["id"])
    return response.json()["id"]  

@pytest.fixture(scope="module")
def setup_order(client, setup_products):
    product_id = setup_products  
    order_data = {
        "items": [
            {"product_id": product_id, "amount": 1} 
        ]
    }
    response = client.post("/orders", json=order_data)
    print("/////////////////////", response.json()) 
    assert response.status_code == 200
    return response.json()["id"] 

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

def test_get_product_by_id(client, setup_products):
    product_id = setup_products  
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    product = response.json()
    assert product["id"] == product_id

def test_update_product(client, setup_products):
    product_update_data = {
        "name": "Updated Product",
        "description": "Updated description",
        "price": 150.0,
        "stock": 20
    }
    product_id = setup_products  
    response = client.put(f"/products/{product_id}", json=product_update_data)
    assert response.status_code == 200
    updated_product = response.json()
    assert updated_product["name"] == product_update_data["name"]

def test_delete_product(client, setup_products):
    product_id = setup_products
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["reply"] == f"product with id {product_id} was deleted"


def test_create_order(client):
    product_4 = client.get("/products/4")
    assert product_4.status_code == 200
    product_5 = client.get("/products/5")
    assert product_5.status_code == 200
    order_data = {
        "items": [
            {"product_id": 4, "amount": 1},
            {"product_id": 5, "amount": 1}
        ]
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json["order_items"], list)
    assert len(response_json["order_items"]) == 2

def test_get_orders(client):
    response = client.get("/orders")
    assert response.status_code == 200
    orders = response.json()
    assert isinstance(orders, list)

def test_get_order_by_id(client, setup_order):
    order_id = setup_order 
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    order = response.json()
    assert order["id"] == order_id


def test_update_order_status(client, setup_order):
    order_id = setup_order 
    new_status = {"status": "shipped"} 
    response = client.patch(f"/orders/{order_id}/status", json=new_status)
    assert response.status_code == 200
    updated_order = response.json()
    assert updated_order["status"] == new_status["status"] 

