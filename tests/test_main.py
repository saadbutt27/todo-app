from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Field, Session, create_engine, select
from app.main import todo_server, get_session, Todo
from app import settings

def test_read_hello():
    client:TestClient = TestClient(app=todo_server)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Greet": "Hello World"}

def test_write_main():
    # Connection to database
    connection_string: str = str(settings.TEST_DATABASE_URL).replace(
        "postgresql", "postgresql+psycopg"
    )

    engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        def get_session_override():
            return session
        
        todo_server.dependency_overrides[get_session] = get_session_override

        client:TestClient = TestClient(app=todo_server)

        todo = Todo(title="test todo", description="my test todo")
        todo_title = "Buy bread"
        todo_description = "Please buy bread"

        response = client.post("/todos",
            json={"title": todo_title, "description": todo_description}
        )

        data = response.json()

        assert response.status_code == 200
        assert data["title"] == todo_title
        assert data["description"] == todo_description

def test_read_list_main():
    # Connection to database
    connection_string: str = str(settings.TEST_DATABASE_URL).replace(
        "postgresql", "postgresql+psycopg"
    )

    engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        def get_session_override():
            return session
        
        todo_server.dependency_overrides[get_session] = get_session_override

        client:TestClient = TestClient(app=todo_server)

        response = client.get("/todos")

        assert response.status_code == 200



def test_hello():
    greet:str = "Hi"
    assert greet == "Hi"