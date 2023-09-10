"""This module contains the projects functions that are used to interact with the database. 

The functions are used by the API routes to perform CRUD operations in the database. Validation of 
the input data is performed by the validators in the input_validators module."""

from datetime import datetime

from sqlalchemy.orm import Session

import app.models.projects as models
import app.schemas.projects as schemas
from app.models.relationships import ProjectCollaborators


def get_project(db: Session, project_id: int) -> models.Project:
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_project_by_name(db: Session, name: str, user_id: int) -> models.Project:
    return db.query(models.Project).filter(models.Project.name == name).first()


def get_owned_and_collaborated_projects(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
) -> list[models.Project]:
    # Query for owned projects
    owned_projects = (
        db.query(models.Project)
        .filter(models.Project.owner_id == user_id)
        .offset(skip)
        .limit(limit)
    )

    # Query for collaborated projects
    collaborated_projects = (
        db.query(models.Project)
        .join(ProjectCollaborators, models.Project.id == ProjectCollaborators.c.project_id)
        .filter(ProjectCollaborators.c.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )

    # Combine the two queries using union
    all_projects = owned_projects.union(collaborated_projects).all()

    return all_projects


def create_project(db: Session, project: schemas.ProjectBase, user_id: int) -> models.Project:
    db_project = models.Project(
        **project.model_dump(),
        owner_id=user_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


def delete_project(db: Session, project_id: int):
    db_project = get_project(db=db, project_id=project_id)

    db.delete(db_project)
    db.commit()


def update_project_information(db: Session, project_id: int, project: schemas.ProjectBase):
    db_project = get_project(db=db, project_id=project_id)

    db_project.name = project.name  # type: ignore
    db_project.description = project.description  # type: ignore
    db_project.updated_at = datetime.now()  # type: ignore

    db.commit()
    db.refresh(db_project)

    return db_project


def add_collaborator(db: Session, project_id: int, user_id: int):
    db_project = get_project(db=db, project_id=project_id)

    # validators.check_valid_project_collaborator(db=db, project_id=project_id, user_id=user_id)

    db_project.collaborators.append(user_id)
    db.commit()
    db.refresh(db_project)

    return db_project
