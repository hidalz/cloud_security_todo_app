"""This module contains all the validators for the input data of the CRUD methods. 

It is used by the API routes to validate the input data before performing any operation in the 
database."""

import re

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.projects import Project
from app.models.tasks import Task
from app.models.users import User

# USER VALIDATORS


def check_valid_email(db: Session, email: str, check_email_is_registered: bool = True):
    # Format checking is performed by Pydantic

    db_email = db.query(User).filter(User.email == email).first()

    if check_email_is_registered and db_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    return True


def check_valid_password(password):
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

    # Check for at least one number, one lowercase and one uppercase letter, and at least one special character
    if not re.match(
        r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+{}|:;<>,.?/~])", password
    ):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one number, one lowercase and one uppercase letter, and at least one special character",
        )

    return True


def check_valid_username(db: Session, username: str):
    if len(username) < 4:
        raise HTTPException(status_code=400, detail="Username must be at least 4 characters long")

    # usernames are case insensitive
    db_user = db.query(User).filter(User.username == username).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    return True


def check_valid_user_id(db: Session, user_id: int):
    if user_id < 0:
        raise HTTPException(status_code=400, detail="User id must be greater or equal to 0")

    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return True


def validate_user(
    db: Session,
    user_id: int | None = None,
    username: str | None = None,
    email: str | None = None,
    check_email_is_registered: bool = True,
    password: str | None = None,
):
    """It performs all the validations for a user depending on the CRUD method. It returns True if
    all validations are passed, otherwise it raises an exception with details inside of each
    validator function."""
    if user_id:
        check_valid_user_id(db=db, user_id=user_id)
    if username:
        check_valid_username(db=db, username=username)
    if email:
        check_valid_email(db=db, email=email, check_email_is_registered=check_email_is_registered)
    if password:
        check_valid_password(password=password)

    return True


# PROJECT VALIDATORS
def check_valid_project_id(
    db: Session, project_id: int, return_db_project=False, user_id: int = None
):
    if project_id < 0:
        raise HTTPException(status_code=400, detail="Project id must be greater or equal to 0")

    db_project = db.query(Project).filter(Project.id == project_id).first()

    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    if user_id and db_project.owner_id != user_id:  # type: ignore
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )

    # For the case of the update_project function, we want to return the db_project
    if return_db_project:
        return db_project

    return True


def check_valid_project_name(db: Session, project_name: str, user_id: int):
    if len(project_name) < 4:
        raise HTTPException(
            status_code=400, detail="Project name must be at least 4 characters long"
        )

    db_project = (
        db.query(Project)
        .filter(Project.owner_id == user_id)  # type: ignore
        .filter(Project.name == project_name)
        .first()
    )

    if db_project:
        raise HTTPException(status_code=400, detail="User already has a project with that name")

    return True


def check_valid_project_collaborator(db: Session, project_id: int, user_id: int):
    check_valid_user_id(db=db, user_id=user_id)

    db_project = check_valid_project_id(
        db=db, project_id=project_id, return_db_project=True, user_id=user_id
    )

    if db_project.owner_id == user_id:  # type: ignore
        raise HTTPException(status_code=400, detail="User is already the owner of this project")

    db_project_collaborator = (
        db.query(Project)
        .join(
            Project.collaborators,
        )
        .filter(Project.id == project_id)
        .filter(Project.collaborators.any(User.id == user_id))  # type: ignore
        .first()
    )

    if db_project_collaborator:
        raise HTTPException(
            status_code=400, detail="User is already a collaborator of this project"
        )

    return True


def validate_project(
    db: Session,
    project_id: int | None = None,
    project_name: str | None = None,
    user_id: int | None = None,
):
    """It performs all the validations for a project depending on the CRUD method. It returns True
    if all validations are passed, otherwise it raises an exception with details inside of each
    validator function."""

    if project_id:
        check_valid_project_id(db=db, project_id=project_id, user_id=user_id)

    if project_name and user_id:
        check_valid_project_name(db=db, project_name=project_name, user_id=user_id)

    if user_id:
        check_valid_user_id(db=db, user_id=user_id)

    return True


# TASK VALIDATORS
def _check_valid_task_priority(task_priority: int):
    if task_priority not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Task priority must be 1, 2 or 3")


def _check_valid_task_id(db: Session, task_id: int, user_id: int):
    if task_id < 0:
        raise HTTPException(status_code=400, detail="Task id must be greater or equal to 0")

    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Should not happen because of the foreign key constraint, but just in case
    if db_task and db_task.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")


def _check_valid_task_parent_id(db: Session, task_parent_id: int):
    if task_parent_id < 0:
        raise HTTPException(
            status_code=400, detail="Task parent id must be greater or equal to 0"
        )

    db_task = db.query(Task).filter(Task.id == task_parent_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task parent not found")


def validate_task(
    db: Session,
    project_id: int | None = None,
    task_id: int | None = None,
    task_parent_id: int | None = None,
    task_priority: int | None = None,
    user_id: int | None = None,
):
    """It performs all the validations for a task depending on the CRUD method. It returns True if
    all validations are passed, otherwise it raises an exception with details inside of each
    validator function."""

    if task_priority:
        _check_valid_task_priority(task_priority=task_priority)

    if task_id and user_id:
        _check_valid_task_id(db=db, task_id=task_id, user_id=user_id)

    if task_parent_id:
        _check_valid_task_parent_id(db=db, task_parent_id=task_parent_id)

    if project_id:
        check_valid_project_id(db=db, project_id=project_id)

    return True
