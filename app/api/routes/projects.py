from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

import app.db.database as db
import app.schemas.projects as project_schema
import app.schemas.users as user_schema
import app.services.projects as project_crud
from app.models.projects import Project as project_model
from app.services.auth import get_current_active_user
from app.services.validators import validate_project

router = APIRouter(tags=["Projects"], prefix="/projects")


@router.get("/", status_code=HTTP_200_OK, response_model=list[project_schema.Project])
def get_owned_and_collaborated_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
) -> list[project_model]:
    return project_crud.get_owned_and_collaborated_projects(
        db, user_id=current_user.id, skip=skip, limit=limit
    )


@router.post("/", status_code=HTTP_201_CREATED, response_model=project_schema.Project)
def create_project(
    project: project_schema.ProjectBase,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
) -> project_model:
    # check_valid_project_name(db=db, project_name=project.name, user_id=current_user.id)
    validate_project(db=db, project_name=project.name, user_id=current_user.id)

    return project_crud.create_project(db, project=project, user_id=current_user.id)


@router.delete("/{project_id}", status_code=HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
) -> None:
    # check_valid_project_id(db=db, project_id=project_id, user_id=current_user.id)
    validate_project(db=db, project_id=project_id, user_id=current_user.id)
    return project_crud.delete_project(db, project_id=project_id)


@router.put("/{project_id}", status_code=HTTP_200_OK, response_model=project_schema.Project)
def update_project(
    project_id: int,
    project: project_schema.ProjectBase,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
) -> project_model:
    validate_project(db=db, project_id=project_id, user_id=current_user.id)

    return project_crud.update_project_information(db, project=project, project_id=project_id)  # type: ignore
