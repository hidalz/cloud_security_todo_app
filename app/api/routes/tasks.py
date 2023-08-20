from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

import app.db.database as db
import app.schemas.users as user_schema
import app.services.tasks as crud
from app.models.tasks import Subtask as subtask_model
from app.models.tasks import Task as task_model
from app.schemas.tasks import Subtask, Task, TaskCreateModify
from app.services import tasks as task_crud
from app.services.auth import get_current_active_user

router = APIRouter(tags=["Tasks"], prefix="/tasks")


@router.get("/", response_model=list[Task])
def read_own_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(db.get_db),
    current_user: task_model = Depends(get_current_active_user),
) -> list[task_model]:
    return crud.get_all_tasks(db, owner_id=current_user.id, skip=skip, limit=limit)  # type: ignore


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
    return task_crud.create_user_task(db=db, task=task, user_id=current_user.id)


# Update task
@router.put("/{task_id}", status_code=HTTP_200_OK, response_model=Task)
def update_task(
    task_id: int,
    task: TaskCreateModify,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
) -> task_model:
    db_task = task_crud.get_task(db, owner_id=current_user.id, task_id=task_id)

    # TODO: Create function to deal with exceptions more elegantly in sepparate module
    if not db_task:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task_crud.update_task(
        db, owner_id=current_user.id, task_id=task_id, task=task
    )


@router.post(
    "/{parent_task_id}", status_code=HTTP_200_OK, response_model=Subtask
)  # TODO: review model and schema output
def create_subtask(
    parent_task_id: int,
    subtask: TaskCreateModify,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(
        get_current_active_user
    ),  # TODO: Find out auth here and if the dependency injection works
) -> subtask_model:
    return task_crud.create_subtask(
        db,
        parent_task_id=parent_task_id,
        subtask=subtask,
    )
