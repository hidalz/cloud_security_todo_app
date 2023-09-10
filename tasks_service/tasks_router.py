"""Tasks routes.

It contains the API routes operations for managing tasks. It validates the input data before,
performing any operation in the database. It does so by using the validators in the validators,
as well as Pydantic models."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

import common_components.database.db as db
import tasks_service.tasks_crud as crud
import users_service.users_schemas as user_schema
from auth_service.auth_crud import get_current_active_user
from common_components.input_validators import validate_task
from tasks_service import tasks_crud as task_crud
from tasks_service.tasks_models import Task as task_model
from tasks_service.tasks_schemas import Task, TaskCreateModify

router = APIRouter(tags=["Tasks"], prefix="/tasks")


@router.get("/", response_model=list[Task])
def get_own_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(db.get_db),
    current_user: task_model = Depends(get_current_active_user),
) -> list[task_model]:
    """Get own tasks.

    Args:
        skip (int, optional): Number of tasks to skip. Defaults to 0.
        limit (int, optional): Number of tasks to return. Defaults to 100.
        db (Session, optional): Database session. Defaults to Depends(db.get_db).
        current_user (task_model, optional): Current user. Defaults to Depends(get_current_active_user).

    Returns:
        list[Task]: List of SQL Alchemy Task models.
    """
    return crud.get_all_own_tasks(db, owner_id=current_user.id, skip=skip, limit=limit)  # type: ignore


@router.post(
    "/",
    status_code=HTTP_201_CREATED,
    response_model=Task,
)
def create_own_task(
    task: TaskCreateModify,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
):
    """Create task.

    Args:
        task (TaskCreateModify): Task data.
        db (Session, optional): Database session. Defaults to Depends(db.get_db).
        current_user (user_schema.User, optional): Current user. Defaults to Depends(get_current_active_user).

    Returns:
        Task: SQL Alchemy Task model.
    """
    validate_task(
        db=db,
        project_id=task.project_id,
        task_parent_id=task.parent_id,
        task_priority=task.priority,
        user_id=current_user.id,
    )

    return task_crud.create_task(db=db, task=task, user_id=current_user.id)


@router.put("/{task_id}", status_code=HTTP_200_OK, response_model=Task)
def update_task(
    task_id: int,
    task: TaskCreateModify,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
) -> task_model:
    """Update task.

    Args:
        task_id (int): Task ID.
        task (TaskCreateModify): Task data.
        db (Session, optional): Database session. Defaults to Depends(db.get_db).
        current_user (user_schema.User, optional): Current user. Defaults to Depends(get_current_active_user).

    Returns:
        task_model: SQL Alchemy Task model.

    Raises:
        HTTPException: If the task does not exist.
        HTTPException: If the user is not the owner of the task.
    """
    validate_task(
        db=db,
        task_priority=task.priority,
        task_id=task_id,
        user_id=current_user.id,
        task_parent_id=task.parent_id,
        project_id=task.project_id,
    )  # type: ignore
    return task_crud.update_task(db, owner_id=current_user.id, task=task, task_id=task_id)


@router.delete("/{task_id}", status_code=HTTP_200_OK)
def delete_task(
    task_id: int,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
):
    """Delete task.

    Args:
        task_id (int): Task ID.
        db (Session, optional): Database session. Defaults to Depends(db.get_db).
        current_user (user_schema.User, optional): Current user. Defaults to Depends(get_current_active_user).

    Raises:
        HTTPException: If the task does not exist.
        HTTPException: If the user is not the owner of the task.
    """
    validate_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )

    db_task = task_crud.get_task(db, owner_id=current_user.id, task_id=task_id)

    if not db_task:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    task_crud.delete_task(db, owner_id=current_user.id, task_id=task_id)

    return {"message": f"Task {task_id} deleted"}
