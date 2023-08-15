from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

import app.db.database as db
import app.services.tasks as crud
from app.models.tasks import Task as task_model
from app.schemas.tasks import Task, TaskBase, TaskCreate
from app.services.auth import get_current_active_user

router = APIRouter(tags=["Tasks"], prefix="/tasks")


@router.get("/", response_model=list[Task])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(db.get_db),
    current_user: task_model = Depends(get_current_active_user),
) -> list[task_model]:
    return crud.get_tasks(db, skip=skip, limit=limit)
