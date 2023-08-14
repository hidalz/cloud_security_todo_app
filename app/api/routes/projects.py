from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import *

import app.db.database as db
import app.services.projects as project_crud
from app.models.projects import Project as project_model
from app.schemas.projects import Project as project_schema

router = APIRouter(tags=["Projects"], prefix="/projects")


@router.get("/", response_model=list[project_schema])
def read_projects(
    skip: int = 0, limit: int = 100, db: Session = Depends(db.get_db)
) -> list[project_model]:
    return project_crud.get_projects(db, skip=skip, limit=limit)
