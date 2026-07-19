import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_register_user():
    response = client.post("/register", json={
        "name": "Teste",
        "email": "teste@pytest.com",
        "password": "123456"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "teste@pytest.com"

def test_register_existing_user():
    client.post("/register", json={
        "name": "Teste",
        "email": "teste@pytest.com",
        "password": "123456"
    })
    response = client.post("/register", json={
        "name": "Teste",
        "email": "teste@pytest.com",
        "password": "123456"
    })
    assert response.status_code == 400

def test_login_success():
    client.post("/register", json={
        "name": "Teste",
        "email": "teste@pytest.com",
        "password": "123456"
    })
    response = client.post("/login", json={
        "email": "teste@pytest.com",
        "password": "123456"
    })
    assert "access_token" in response.json()