from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import *

import app.db.database as db
import app.models.users as user_model
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


#### USERS ####
@router.get("/me/", response_model=user_schema.User)
async def read_users_me(
    current_user: user_schema.User = Depends(get_current_active_user),
):
    return current_user  # TODO: Esto devuelve subtasks como tasks, ver como arreglarlo
