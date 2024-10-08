# docker run -d --rm --name postgres -e POSTGRES_DB=todo -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:16-alpine
# docker run -d --rm --name otelcol -p 4317:4317 otel/opentelemetry-collector-contrib:latest

import os
from datetime import datetime
from typing import List, Optional, Annotated, AsyncGenerator, Any
from sqlmodel import Field, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, field_validator
from contextlib import asynccontextmanager
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

db_host = os.getenv("POSTGRES_HOST", "localhost")
db_port = os.getenv("POSTGRES_PORT", "5432")
db_name = os.getenv("POSTGRES_DB", "todo")
db_user = os.getenv("POSTGRES_USER", "postgres")
db_passwd = os.getenv("POSTGRES_PASSWORD", "postgres")
db_url = f"postgresql+asyncpg://{db_user}:{db_passwd}@{db_host}:{db_port}/{db_name}"

engine = create_async_engine(db_url, echo=True, future=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

app = FastAPI(
    title="TODO API",
    version="0.1.0",
    contact={"name": "Alejandro Galue"},
    lifespan=lifespan
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    title: str
    description: Optional[str]
    priority: int
    completed: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now())

class TodoAdd(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int

    @field_validator('priority')
    def priority_check(cls, value: int) -> int:
        if value < 1 or value > 5:
            raise ValueError('The priority must be a number between 1 and 5')
        return value

    model_config = ConfigDict(
        json_schema_extra = {
            'examples': [
                {
                    'title': 'Learn Python',
                    'description': 'It is never late to learn something great',
                    'priority': 1,
                }
            ]
        }
    )

class HealthCheck(BaseModel):
    status: str = "OK"

class TodoUpdate(BaseModel):
    completed: bool = False

async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    async with AsyncSession(engine) as session:
        yield session

async def get_todo(id: int, db: AsyncSession) -> Todo:
    result = await db.execute(select(Todo).where(Todo.id == id))
    todo = result.scalar_one_or_none()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

DB = Annotated[AsyncSession, Depends(get_db)]

@app.get("/health", summary="Perform a Health Check", tags=["healthcheck"])
async def get_health() -> HealthCheck:
    return HealthCheck(status="OK")

@app.post("/todos/", status_code=status.HTTP_201_CREATED)
async def create_todo(src: TodoAdd, db: DB) -> Todo:
    todo = Todo(**src.model_dump())
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo

@app.get("/todos/")
async def read_todos(db: DB) -> List[Todo]:
    result = await db.execute(select(Todo))
    return result.scalars().all()

@app.get("/todos/{id}")
async def read_todo(id: int, db: DB) -> Todo:
    result = await get_todo(id, db)
    return result

@app.put("/todos/{id}")
async def update_todo(id: int, src: TodoUpdate, db: DB) -> Todo:
    todo = await get_todo(id, db)
    for key, value in src.model_dump().items():
        setattr(todo, key, value)
    await db.commit()
    await db.refresh(todo)
    return todo

@app.delete("/todos/{id}")
async def delete_todo(id: int, db: DB) -> Todo:
    todo = await get_todo(id, db)
    await db.delete(todo)
    await db.commit()
    return todo

LoggingInstrumentor().instrument(set_logging_format=True)
FastAPIInstrumentor.instrument_app(app)
SQLAlchemyInstrumentor().instrument(
    engine=engine.sync_engine,
    enable_commenter=True,
    commenter_options={}
)
