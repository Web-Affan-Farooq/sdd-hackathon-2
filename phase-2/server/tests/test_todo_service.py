import pytest
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.todo import Todo, TodoStatus
from app.schemas.todo import TodoCreate, TodoUpdate, TodoRead
from app.services.todo_service import (
    create_todo,
    get_todo_by_id,
    get_todos,
    update_todo,
    delete_todo
)
from unittest.mock import Mock, AsyncMock


@pytest.mark.asyncio
async def test_create_todo():
    """Test creating a new todo."""
    # Arrange
    todo_create = TodoCreate(
        title="Test Todo",
        description="Test Description",
        user_id=1
    )

    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    # Act
    result = await create_todo(todo_create, mock_session)

    # Assert
    assert isinstance(result, Todo)
    assert result.title == "Test Todo"
    assert result.description == "Test Description"
    assert result.user_id == 1
    assert result.status == TodoStatus.pending
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_get_todo_by_id():
    """Test retrieving a todo by ID."""
    # Arrange
    todo_id = 1
    user_id = 1
    expected_todo = Todo(
        id=todo_id,
        title="Test Todo",
        description="Test Description",
        user_id=user_id,
        status=TodoStatus.pending
    )

    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = AsyncMock()
    mock_result.first.return_value = expected_todo
    mock_session.exec.return_value = mock_result

    # Act
    result = await get_todo_by_id(todo_id, user_id, mock_session)

    # Assert
    assert result == expected_todo


@pytest.mark.asyncio
async def test_get_todos():
    """Test retrieving all todos for a user."""
    # Arrange
    user_id = 1
    expected_todos = [
        Todo(id=1, title="Todo 1", description="Desc 1", user_id=user_id, status=TodoStatus.pending),
        Todo(id=2, title="Todo 2", description="Desc 2", user_id=user_id, status=TodoStatus.completed)
    ]

    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = AsyncMock()
    mock_result.all.return_value = expected_todos
    mock_session.exec.return_value = mock_result

    # Act
    result = await get_todos(user_id, mock_session)

    # Assert
    assert result == expected_todos


@pytest.mark.asyncio
async def test_update_todo():
    """Test updating a todo."""
    # Arrange
    todo_id = 1
    user_id = 1
    todo_update = TodoUpdate(title="Updated Title")
    existing_todo = Todo(
        id=todo_id,
        title="Old Title",
        description="Old Description",
        user_id=user_id,
        status=TodoStatus.pending
    )

    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = AsyncMock()
    mock_result.first.return_value = existing_todo
    mock_session.exec.return_value = mock_result
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    # Act
    result = await update_todo(todo_id, user_id, todo_update, mock_session)

    # Assert
    assert result.title == "Updated Title"
    assert result.description == "Old Description"  # Should remain unchanged
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_todo():
    """Test deleting a todo."""
    # Arrange
    todo_id = 1
    user_id = 1
    existing_todo = Todo(
        id=todo_id,
        title="To Delete",
        description="To Delete Desc",
        user_id=user_id,
        status=TodoStatus.pending
    )

    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = AsyncMock()
    mock_result.first.return_value = existing_todo
    mock_session.exec.return_value = mock_result
    mock_session.delete.return_value = None
    mock_session.commit.return_value = None

    # Act
    result = await delete_todo(todo_id, user_id, mock_session)

    # Assert
    assert result is True
    mock_session.delete.assert_called_once_with(existing_todo)
    mock_session.commit.assert_called_once()