from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

import app.db.database as db
import app.schemas.users as user_schema
import app.services.tasks as crud
from app.models.tasks import Task as task_model
from app.schemas.tasks import Task, TaskCreateModify
from app.services import tasks as task_crud
from app.services.auth import get_current_active_user

router = APIRouter(tags=["Tasks"], prefix="/tasks")


@router.get("/", response_model=list[Task])
def get_own_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(db.get_db),
    current_user: task_model = Depends(get_current_active_user),
) -> list[task_model]:
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
    return task_crud.create_task(db=db, task=task, user_id=current_user.id)


# Update task
@router.put("/{task_id}", status_code=HTTP_200_OK, response_model=Task)
def update_task(
    task: TaskCreateModify,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
) -> task_model:
    db_task = task_crud.get_task(db, owner_id=current_user.id, task_id=task.id)

    # TODO: Create function to deal with exceptions more elegantly in sepparate module
    if not db_task:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task_crud.update_task(db, owner_id=current_user.id, task=task)


@router.delete("/{task_id}", status_code=HTTP_200_OK)
def delete_task(
    task_id: int,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
):
    task_crud.delete_task(
        db, owner_id=current_user.id, task_id=task_id
    )  # Review current user id needed or not. OVerkill. TODO
    return {"message": f"Task {task_id} deleted"}
