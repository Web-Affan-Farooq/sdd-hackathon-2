from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from ..database.database import get_session
from ..models.todo import Todo, TodoStatus
from ..schemas.todo import TodoCreate, TodoUpdate, TodoRead
from ..auth.auth import get_current_user_id
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from ..services.todo_service import (
    create_todo,
    get_todos,
    get_todo_by_id,
    update_todo,
    delete_todo
)


router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=TodoRead, status_code=201)
async def create_todo(
    todo: TodoCreate,
    session: AsyncSession = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id),
):
    # Ensure user can only create todos for themselves
    if todo.user_id != current_user_id:
        raise HTTPException(
            status_code=403,
            detail="Cannot create todo for another user"
        )

    return await create_todo(todo, session)


@router.get("/", response_model=List[TodoRead])
async def list_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: TodoStatus | None = Query(None),
    title_contains: str | None = Query(None, description="Filter by title containing the specified text"),
    sort_by: str = Query("created_at", description="Sort by field: created_at, updated_at, title"),
    sort_order: str = Query("desc", description="Sort order: asc or desc"),
    session: AsyncSession = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id),
):
    return await get_todos(
        user_id=current_user_id,
        session=session,
        skip=skip,
        limit=limit,
        status=status,
        title_contains=title_contains,
        sort_by=sort_by,
        sort_order=sort_order
    )


@router.get("/{todo_id}", response_model=TodoRead)
async def get_todo(
    todo_id: int,
    session: AsyncSession = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id),
):
    todo = await get_todo_by_id(todo_id, current_user_id, session)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo


@router.put("/{todo_id}", response_model=TodoRead)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    session: AsyncSession = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id),
):
    updated_todo = await update_todo(todo_id, current_user_id, todo_update, session)

    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return updated_todo


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: int,
    session: AsyncSession = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id),
):
    success = await delete_todo(todo_id, current_user_id, session)

    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")

    return {"message": "Todo deleted successfully"}