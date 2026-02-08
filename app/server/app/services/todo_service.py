from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.todo import Todo, TodoStatus
from app.schemas.todo import TodoCreate, TodoUpdate, TodoRead
from datetime import datetime


async def create_todo(todo: TodoCreate, session: AsyncSession) -> Todo:
    """Create a new todo."""
    db_todo = Todo.model_validate(todo)
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    return db_todo


async def get_todo_by_id(todo_id: int, user_id: int, session: AsyncSession) -> Optional[Todo]:
    """Get a todo by ID for a specific user."""
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    result = await session.exec(statement)
    return result.first()


async def get_todos(
    user_id: int,
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    status: Optional[TodoStatus] = None,
    title_contains: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> List[Todo]:
    """Get all todos for a specific user with optional filters and sorting."""
    statement = select(Todo).where(Todo.user_id == user_id)

    if status:
        statement = statement.where(Todo.status == status)

    if title_contains:
        statement = statement.where(Todo.title.contains(title_contains))

    # Apply sorting
    if sort_by == "created_at":
        order_column = Todo.created_at
    elif sort_by == "updated_at":
        order_column = Todo.updated_at
    elif sort_by == "title":
        order_column = Todo.title
    else:
        order_column = Todo.created_at

    if sort_order == "desc":
        statement = statement.order_by(order_column.desc())
    else:
        statement = statement.order_by(order_column.asc())

    statement = statement.offset(skip).limit(limit)

    result = await session.exec(statement)
    return result.all()


async def update_todo(todo_id: int, user_id: int, todo_update: TodoUpdate, session: AsyncSession) -> Optional[Todo]:
    """Update a todo."""
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    result = await session.exec(statement)
    db_todo = result.first()

    if not db_todo:
        return None

    # Update fields that were provided
    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)

    db_todo.updated_at = datetime.utcnow()

    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)

    return db_todo


async def delete_todo(todo_id: int, user_id: int, session: AsyncSession) -> bool:
    """Delete a todo."""
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    result = await session.exec(statement)
    db_todo = result.first()

    if not db_todo:
        return False

    await session.delete(db_todo)
    await session.commit()

    return True