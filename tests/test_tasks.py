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

@pytest.fixture
def auth_headers():
    client.post("/register", json={
        "name": "Teste",
        "email": "teste@pytest.com",
        "password": "123456"
    })
    response = client.post("/login", json={
        "email": "teste@pytest.com",
        "password": "123456"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_task(auth_headers):
    response = client.post("/tasks", json={
        "title": "Tarefa de teste",
        "description": "Descricao de teste"
    }, headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["title"] == "Tarefa de teste"

def test_list_tasks(auth_headers):
    client.post("/tasks", json={
        "title": "Tarefa de teste",
        "description": "Descricao de teste"
    }, headers=auth_headers)

    response = client.get("/tasks", headers=auth_headers)

    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_task(auth_headers):
    create_response = client.post("/tasks", json={
        "title": "Tarefa de teste",
        "description": "Descricao de teste"
    }, headers=auth_headers)

    task_id = create_response.json()["id"]

    update_response = client.put(f"/tasks/{task_id}", json={
        "title": "Tarefa atualizada",
        "description": "Descricao atualizada"
    }, headers=auth_headers)

    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Tarefa atualizada"

def test_delete_task(auth_headers):
    create_response = client.post("/tasks", json={
        "title": "Tarefa de teste",
        "description": "Descricao de teste"
    }, headers=auth_headers)

    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}", headers=auth_headers)

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Tarefa deletada com sucesso"

def test_create_task_without_auth():
    response = client.post("/tasks", json={
        "title": "Tarefa sem auth",
        "description": "Não deveria funcionar"
    })
    assert response.status_code == 401