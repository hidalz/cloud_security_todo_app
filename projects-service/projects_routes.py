"""Projects routes.

It contains the API routes operations for managing projects. It validates the input data before,
performing any operation in the database. It does so by using the validators in the validators,
as well as Pydantic models."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

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
    """Get owned and collaborated projects.

    Args:
        skip (int, optional): Number of projects to skip. Defaults to 0.
        limit (int, optional): Number of projects to return. Defaults to 100.
        db (Session, optional): Database session. Defaults to Depends(db.get_db).
        current_user (user_schema.User, optional): Current user. Defaults to Depends(get_current_active_user).

    Returns:
        list[Project]: List of SQL Alchemy Project models.
    """
    return project_crud.get_owned_and_collaborated_projects(
        db, user_id=current_user.id, skip=skip, limit=limit
    )


@router.post("/", status_code=HTTP_201_CREATED, response_model=project_schema.Project)
def create_project(
    project: project_schema.ProjectBase,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
) -> project_model:
    """Create project.

    Args:
        project (project_schema.ProjectBase): Project data.
        db (Session, optional): Database session. Defaults to Depends(db.get_db).
        current_user (user_schema.User, optional): Current user. Defaults to Depends(get_current_active_user).

    Returns:
        project_model: SQL Alchemy Project model.

    Raises:
        HTTPException: If the project name already exists.
    """
    validate_project(db=db, project_name=project.name, user_id=current_user.id)
    return project_crud.create_project(db, project=project, user_id=current_user.id)


@router.delete("/{project_id}", status_code=HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
) -> None:
    """Delete project.

    Args:
        project_id (int): Project ID.
        db (Session, optional): Database session. Defaults to Depends(db.get_db).
        current_user (user_schema.User, optional): Current user. Defaults to Depends(get_current_active_user).

    Raises:
        HTTPException: If the project does not exist.
        HTTPException: If the user is not the owner of the project.
    """
    validate_project(db=db, project_id=project_id, user_id=current_user.id)
    return project_crud.delete_project(db, project_id=project_id)


@router.put("/{project_id}", status_code=HTTP_200_OK, response_model=project_schema.Project)
def update_project(
    project_id: int,
    project: project_schema.ProjectBase,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
) -> project_model:
    """Update project.

    Args:
        project_id (int): Project ID.
        project (project_schema.ProjectBase): Project data.
        db (Session, optional): Database session. Defaults to Depends(db.get_db).
        current_user (user_schema.User, optional): Current user. Defaults to Depends(get_current_active_user).

    Returns:
        project_model: SQL Alchemy Project model.

    Raises:
        HTTPException: If the project does not exist.
        HTTPException: If the user is not the owner of the project.
    """
    validate_project(db=db, project_id=project_id, user_id=current_user.id)

    return project_crud.update_project_information(db, project=project, project_id=project_id)  # type: ignore
