from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import *

import app.db.database as db
import app.schemas.projects as project_schema
import app.schemas.users as user_schema
import app.services.projects as project_crud
from app.models.projects import (
    Project as project_model,  # TODO: Why returning models y not schemas?
)
from app.services.auth import get_current_active_user

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
    return project_crud.create_project(db, project=project, user_id=current_user.id)


@router.delete("/{project_id}", status_code=HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
) -> None:
    db_project = project_crud.get_project(db, project_id=project_id)  # type: ignore #TODO: verificacion de que sea proyecto suyo

    if not db_project:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    if db_project.owner_id != current_user.id:  # type: ignore
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    # AHHHH SE HACEN LAS COMPROBACIONES AQUI CON UN RAISE EXCEPTION, ELSE LA OPERACION DEL CRUD SOLO SE HACE SI PASA LAS COMPROBACIONES
    # TODO: BIG BRAIN TIME. Checkear el otro proyecto y si hace lo mismo y fastapi docu
    return project_crud.delete_project(db, project_id=project_id)


@router.put(
    "/{project_id}", status_code=HTTP_200_OK, response_model=project_schema.Project
)
def update_project(
    project_id: int,
    project: project_schema.ProjectBase,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
) -> project_model:
    db_project = project_crud.get_project(db, project_id=project_id)

    if not db_project:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    if db_project.owner_id != current_user.id:  # type: ignore
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    return project_crud.update_project_information(db, project=project, project_id=project_id)  # type: ignore
