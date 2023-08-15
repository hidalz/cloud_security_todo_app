from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import *

import app.db.database as db
import app.schemas.projects as project_schema
import app.schemas.tasks as task_schema
import app.schemas.users as user_schema
import app.services.projects as project_crud
import app.services.tasks as task_crud
import app.services.users as user_crud
from app.services.auth import get_current_active_user

router = APIRouter(tags=["Users"], prefix="/users")

# TODO: Create ADMIN user and add permissions to CRUD users


@router.post("/", status_code=HTTP_201_CREATED, response_model=user_schema.User)
def create_user(user: user_schema.UserInDB, db: Session = Depends(db.get_db)):
    db_user = user_crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return user_crud.create_user(db=db, user=user)


@router.get("/", status_code=HTTP_200_OK, response_model=list[user_schema.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", status_code=HTTP_200_OK, response_model=user_schema.User)
def read_user(
    user_id: int,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
):
    db_user = user_crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post(
    "/{user_id}/tasks/",
    status_code=HTTP_201_CREATED,
    response_model=task_schema.Task,
)
def create_task_for_user(
    user_id: int,
    task: task_schema.TaskCreate,
    db: Session = Depends(db.get_db),
):  # TODO: review current_user y como settear el id
    return task_crud.create_user_task(db=db, task=task, user_id=user_id)


@router.post(
    "/{user_id}/projects/",
    status_code=HTTP_201_CREATED,
    response_model=project_schema.Project,
)
def create_project_for_user(
    user_id: int,
    project: project_schema.ProjectBase,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
):
    return project_crud.create_user_project(db=db, project=project, user_id=user_id)


#### USERS ####
@router.get("/me/", response_model=user_schema.User)
async def read_users_me(
    current_user: user_schema.User = Depends(get_current_active_user),
):
    return current_user


@router.get("/me/tasks/")
async def read_own_items(
    current_user: user_schema.User = Depends(get_current_active_user),
):
    return [{"item_id": "Foo", "owner": current_user.username}]
