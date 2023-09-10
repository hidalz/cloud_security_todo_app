"""This module contains all the validators for the input data of the CRUD methods. 

It is used by the API routes to validate the input data before performing any operation in the 
database."""

import re

from fastapi import HTTPException
from sqlalchemy.orm import Session

from projects_service.projects_models import Project
from tasks_service.tasks_models import Task
from users_service.users_models import User

# USER VALIDATORS


def check_valid_email(db: Session, email: str, check_email_is_registered: bool = True) -> bool:
    """Check that the email is valid and not already registered in the database.

    Args:
        db (Session): Database session.
        email (str): Email to check.
        check_email_is_registered (bool, optional): Whether to check if the email is already
            registered in the database. Defaults to True.

    Returns:
        bool: True if the email is valid and not already registered in the database.

    Raises:
        HTTPException: If the email is already registered in the database.
    """

    # Format checking is performed by Pydantic

    db_email = db.query(User).filter(User.email == email).first()

    if check_email_is_registered and db_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    return True


def check_valid_password(password: str) -> bool:
    """Check that the password is valid.

    Args:
        password (str): Password to check.

    Returns:
        bool: True if the password is valid.

    Raises:
        HTTPException: If the password is not valid.
    """
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


def check_valid_username(db: Session, username: str) -> bool:
    """Check that the username is valid and not already registered in the database.

    Args:
        db (Session): Database session.
        username (str): Username to check.

    Returns:
        bool: True if the username is valid and not already registered in the database.

    Raises:
        HTTPException: If the username is not valid or already registered in the database.
    """
    if len(username) < 4:
        raise HTTPException(status_code=400, detail="Username must be at least 4 characters long")

    # usernames are case insensitive
    db_user = db.query(User).filter(User.username == username).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    return True


def check_valid_user_id(db: Session, user_id: int) -> bool:
    """Check that the user id is valid and registered in the database.

    Args:
        db (Session): Database session.
        user_id (int): User id to check.

    Returns:
        bool: True if the user id is valid and registered in the database.

    Raises:
        HTTPException: If the user id is not valid or not registered in the database.
    """
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
) -> bool:
    """It performs all the validations for a user depending on the CRUD method.

    It returns True if all validations are passed, otherwise it raises an exception with details
    inside of each validator function.

    Args:
        db (Session): Database session.
        user_id (int, optional): User id. Defaults to None.
        username (str, optional): Username. Defaults to None.
        email (str, optional): Email. Defaults to None.
        check_email_is_registered (bool, optional): Whether to check if the email is already
            registered in the database. Defaults to True.
        password (str, optional): Password. Defaults to None.

    Returns:
        bool: True if all validations are passed.

    Raises:
        HTTPException: If any of the validations fails.
    """

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
) -> bool | Project:
    """Check that the project id is valid and registered in the database.

    Args:
        db (Session): Database session.
        project_id (int): Project id to check.
        return_db_project (bool, optional): Whether to return the db_project object. Defaults to False.
        user_id (int, optional): User id. Defaults to None.

    Returns:
        bool: True if the project id is valid and registered in the database.
        Project: Project SQLAlchemy model, only if return_db_project is True. Defaults to None.

    Raises:
        HTTPException: If the project id is not valid or not registered in the database.
    """
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


def check_valid_project_name(db: Session, project_name: str, user_id: int) -> bool:
    """Check that the project name is valid and not already registered in the database.

    Args:
        db (Session): Database session.
        project_name (str): Project name to check.
        user_id (int): User id.

    Returns:
        bool: True if the project name is valid and not already registered in the database.

    Raises:
        HTTPException: If the project name is not valid or already registered in the database.
    """
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


def check_valid_project_collaborator(db: Session, project_id: int, user_id: int) -> bool:
    """Check that the user is not already the owner or a collaborator of the project.

    Args:
        db (Session): Database session.
        project_id (int): Project id.
        user_id (int): User id.

    Returns:
        bool: True if the user is not already the owner or a collaborator of the project.

    Raises:
        HTTPException: If the user is already the owner or a collaborator of the project.
    """
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
) -> bool:
    """It performs all the validations for a project depending on the CRUD method. It returns True
    if all validations are passed, otherwise it raises an exception with details inside of each
    validator function.

    Args:
        db (Session): Database session.
        project_id (int, optional): Project id. Defaults to None.
        project_name (str, optional): Project name. Defaults to None.
        user_id (int, optional): User id. Defaults to None.

    Returns:
        bool: True if all validations are passed.

    Raises:
        HTTPException: If any of the validations fails.
    """

    if project_id:
        check_valid_project_id(db=db, project_id=project_id, user_id=user_id)

    if project_name and user_id:
        check_valid_project_name(db=db, project_name=project_name, user_id=user_id)

    if user_id:
        check_valid_user_id(db=db, user_id=user_id)

    return True


# TASK VALIDATORS
def _check_valid_task_priority(task_priority: int) -> None:
    """Check that the task priority is valid.

    Args:
        task_priority (int): Task priority.

    Raises:
        HTTPException: If the task priority is not valid."""
    if task_priority not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Task priority must be 1, 2 or 3")


def _check_valid_task_id(db: Session, task_id: int, user_id: int) -> None:
    """Check that the task id is valid and registered in the database.

    Args:
        db (Session): Database session.
        task_id (int): Task id to check.
        user_id (int): User id.

    Raises:
        HTTPException: If the task id is not valid or not registered in the database.
    """
    if task_id < 0:
        raise HTTPException(status_code=400, detail="Task id must be greater or equal to 0")

    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Should not happen because of the foreign key constraint, but just in case
    if db_task and db_task.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")


def _check_valid_task_parent_id(db: Session, task_parent_id: int):
    """Check that the task parent id is valid and registered in the database.

    Args:
        db (Session): Database session.
        task_parent_id (int): Task parent id to check.

    Raises:
        HTTPException: If the task parent id is not valid or not registered in the database.
    """
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
    validator function.

    Args:
        db (Session): Database session.
        project_id (int, optional): Project id. Defaults to None.
        task_id (int, optional): Task id. Defaults to None.
        task_parent_id (int, optional): Task parent id. Defaults to None.
        task_priority (int, optional): Task priority. Defaults to None.
        user_id (int, optional): User id. Defaults to None.

    Returns:
        bool: True if all validations are passed.

    Raises:
        HTTPException: If any of the validations fails.
    """

    if task_priority:
        _check_valid_task_priority(task_priority=task_priority)

    if task_id and user_id:
        _check_valid_task_id(db=db, task_id=task_id, user_id=user_id)

    if task_parent_id:
        _check_valid_task_parent_id(db=db, task_parent_id=task_parent_id)

    if project_id:
        check_valid_project_id(db=db, project_id=project_id)

    return True
