from fastapi import FastAPI, Depends
from typing import Annotated
from sqlmodel import SQLModel, Session, select
from app.models import Todo
from app.db import engine
from contextlib import asynccontextmanager

def create_db_tables():
    print("creating tables")
    SQLModel.metadata.create_all(engine)
    print("done")

@asynccontextmanager
async def life_span(todo_server: FastAPI):
    print("Server startup")
    create_db_tables()
    yield 


todo_server:FastAPI = FastAPI(lifespan=life_span)

def get_session():
    with Session(engine) as session:
        yield session


@todo_server.get("/")
def root():
    return {"Greet": "Hello World"}

# @todo_server.get("/db")
# def db_var():
#     return {"DB": settings.DATABASE_URL, "Connection": connection_string}

@todo_server.post("/todos")
def create_todo(todo_data: Todo, session:Annotated[Session, Depends(get_session)]):
    session.add(todo_data)
    session.commit()
    session.refresh(todo_data)
    return todo_data
    
@todo_server.get("/todos")
def get_all_todos(session:Annotated[Session, Depends(get_session)]):
        query = select(Todo)
        all_todos = session.exec(query).all()
        return all_todos

@todo_server.get("/todos/{todo_id}")
def get_todo(todo_id:int, session:Annotated[Session, Depends(get_session)]):
        query = select(Todo).where(Todo.id == todo_id)
        all_todos = session.exec(query).all()
        return all_todos
