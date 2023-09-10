"""This module contains the projects functions that are used to interact with the database. 

The functions are used by the API routes to perform CRUD operations in the database. Validation of 
the input data is performed by the validators in the input_validators module."""

from datetime import datetime

from sqlalchemy.orm import Session

import projects_service.projects_models as models
import projects_service.projects_schemas as schemas
from common_components.database.models_relationships import ProjectCollaborators


def get_project(db: Session, project_id: int) -> models.Project:
    """Get project by ID.

    Args:
        db (Session): Database session.
        project_id (int): Project ID.

    Returns:
        models.Project: SQL Alchemy Project model.
    """
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_project_by_name(db: Session, name: str) -> models.Project:
    """Get project by name.

    Args:
        db (Session): Database session.
        name (str): Project name.

    Returns:
        models.Project: SQL Alchemy Project model.
    """
    return db.query(models.Project).filter(models.Project.name == name).first()


def get_owned_and_collaborated_projects(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
) -> list[models.Project]:
    """Get owned and collaborated projects.

    Args:
        db (Session): Database session.
        user_id (int): User ID.
        skip (int, optional): Number of projects to skip. Defaults to 0.
        limit (int, optional): Number of projects to return. Defaults to 100.

    Returns:
        list[Project]: List of SQL Alchemy Project models.
    """

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
    """Create project.

    Args:
        db (Session): Database session.
        project (schemas.ProjectBase): Project data.
        user_id (int): User ID.

    Returns:
        models.Project: SQL Alchemy Project model.

    Raises:
        HTTPException: If the project name already exists.
    """

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


def delete_project(db: Session, project_id: int) -> None:
    """Delete project.

    Args:
        db (Session): Database session.
        project_id (int): Project ID.

    Raises:
        HTTPException: If the project does not exist.
        HTTPException: If the user is not the owner of the project.
    """
    db_project = get_project(db=db, project_id=project_id)

    db.delete(db_project)
    db.commit()


def update_project_information(
    db: Session, project_id: int, project: schemas.ProjectBase
) -> models.Project:
    """Update project information.

    Args:
        db (Session): Database session.
        project_id (int): Project ID.
        project (schemas.ProjectBase): Project data.

    Returns:
        models.Project: SQL Alchemy Project model.
    """

    db_project = get_project(db=db, project_id=project_id)

    db_project.name = project.name  # type: ignore
    db_project.description = project.description  # type: ignore
    db_project.updated_at = datetime.now()  # type: ignore

    db.commit()
    db.refresh(db_project)

    return db_project


def add_collaborator(db: Session, project_id: int, user_id: int) -> models.Project:
    """Add collaborator to project.

    Args:
        db (Session): Database session.
        project_id (int): Project ID.
        user_id (int): User ID.

    Returns:
        models.Project: SQL Alchemy Project model.
    """

    db_project = get_project(db=db, project_id=project_id)

    # validators.check_valid_project_collaborator(db=db, project_id=project_id, user_id=user_id)

    db_project.collaborators.append(user_id)
    db.commit()
    db.refresh(db_project)

    return db_project
