from fastapi.testclient import TestClient
from app.main import todo_server

client:TestClient = TestClient(app=todo_server)

def test_fastapi_hello():
    response = client.get("/")
    assert response.json() == {"Greet": "Hello World"}

def test_hello():
    greet:str = "Hi"
    assert greet == "Hi"