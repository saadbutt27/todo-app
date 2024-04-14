from sqlmodel import SQLModel, Field

# Databse table schema
class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str