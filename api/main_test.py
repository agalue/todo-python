import pytest
from typing import Any, AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient, ASGITransport
from .main import app, get_db

# Use SQLite in-memory for tests
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create a new engine using SQLite for testing purposes
test_engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create a sessionmaker that binds to the test engine
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine, class_=AsyncSession)

# Override the get_db dependency to use the SQLite in-memory session
async def override_get_db() -> AsyncGenerator[AsyncSession, Any]:
    async with TestSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
async def setup_db():
    # Create the tables in the test database
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    # Cleanup tables after tests
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

@pytest.mark.asyncio
async def test_create_todo(setup_db):
    todo_data = {
        "title": "Test Todo",
        "description": "A test todo description",
        "priority": 3
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/todos/", json=todo_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == todo_data["title"]
    assert data["description"] == todo_data["description"]
    assert data["priority"] == todo_data["priority"]
    assert data["completed"] is False

@pytest.mark.asyncio
async def test_read_todos(setup_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/todos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_read_todo_not_found(setup_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/todos/999")  # Non-existent ID
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}

@pytest.mark.asyncio
async def test_update_todo(setup_db):
    todo_data = {
        "title": "Test Todo Update",
        "description": "A test todo update",
        "priority": 2
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # First create a todo
        create_response = await ac.post("/todos/", json=todo_data)
        todo_id = create_response.json()["id"]

        # Now update the todo
        update_data = {"completed": True}
        update_response = await ac.put(f"/todos/{todo_id}", json=update_data)
        assert update_response.status_code == 200
        updated_todo = update_response.json()
        assert updated_todo["completed"] is True

@pytest.mark.asyncio
async def test_delete_todo(setup_db):
    todo_data = {
        "title": "Test Todo Delete",
        "description": "A test todo to be deleted",
        "priority": 1
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # First create a todo
        create_response = await ac.post("/todos/", json=todo_data)
        todo_id = create_response.json()["id"]

        # Delete the todo
        delete_response = await ac.delete(f"/todos/{todo_id}")
        assert delete_response.status_code == 200
        deleted_todo = delete_response.json()
        assert deleted_todo["id"] == todo_id

        # Verify deletion
        get_response = await ac.get(f"/todos/{todo_id}")
        assert get_response.status_code == 404
