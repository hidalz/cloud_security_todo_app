import re

from fastapi import (
    HTTPException,  # Test validators instead of directly testing the api against different outcomes?? idk; TODO: Check if should do error handling in CRUD, routing or validators. Reuse them all in this module and raise exception to the routing
)
from sqlalchemy.orm import Session

from app.models.projects import Project
from app.models.tasks import Task
from app.models.users import User

# USER VALIDATORS


def check_valid_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise HTTPException(status_code=400, detail="Invalid email address")

    return True


def check_valid_password(password):
    if len(password) < 8:
        raise HTTPException(
            status_code=400, detail="Password must be at least 8 characters long"
        )

    # Check for at least one number, one lowercase and one uppercase letter, and at least one special character
    if not re.match(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]", password
    ):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one number, one lowercase and one uppercase letter, and at least one special character",
        )

    return True


def check_valid_username(username):
    if len(username) < 4:
        raise HTTPException(
            status_code=400, detail="Username must be at least 4 characters long"
        )

    return True


def check_valid_user_id(db: Session, user_id: int):
    if user_id < 0:
        raise HTTPException(
            status_code=400, detail="User id must be greater or equal to 0"
        )

    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return True


# PROJECT VALIDATORS
def check_valid_project_id(db: Session, project_id: int, return_db_project=False):
    if project_id < 0:
        raise HTTPException(
            status_code=400, detail="Project id must be greater or equal to 0"
        )

    db_project = db.query(Project).filter(Project.id == project_id).first()

    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

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
        raise HTTPException(
            status_code=400, detail="User already has a project with that name"
        )

    return True


def check_valid_project_collaborator(db: Session, project_id: int, user_id: int):
    check_valid_user_id(db=db, user_id=user_id)

    db_project = check_valid_project_id(
        db=db, project_id=project_id, return_db_project=True
    )

    if db_project.owner_id == user_id:  # type: ignore
        raise HTTPException(
            status_code=400, detail="User is already the owner of this project"
        )

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


# TASK VALIDATORS


def _check_valid_task_priority(task_priority: int):
    if task_priority not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Task priority must be 1, 2 or 3")

    return True


def _check_valid_task_id(db: Session, task_id: int):
    if task_id < 0:
        raise HTTPException(
            status_code=400, detail="Task id must be greater or equal to 0"
        )

    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return True


def _check_valid_task_parent_id(db: Session, task_parent_id: int):
    if task_parent_id < 0:
        raise HTTPException(
            status_code=400, detail="Task parent id must be greater or equal to 0"
        )

    db_task = db.query(Task).filter(Task.id == task_parent_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task parent not found")

    return True


def validate_task(
    db: Session,
    project_id: int | None = None,
    task_id: int | None = None,
    task_parent_id: int | None = None,
    task_priority: int | None = None,
):
    """It performs all the validations for a task depending on the CRUD method. It returns True if
    all validations are passed, otherwise it raises an exception with details inside of each
    validator function."""
    validations = {
        "task_id": (task_id, _check_valid_task_id),
        "task_parent_id": (task_parent_id, _check_valid_task_parent_id),
        "task_priority": (task_priority, _check_valid_task_priority),
        "project_id": (project_id, check_valid_project_id),
    }

    valid_results = []
    for value, validator in validations.values():
        if value is None:
            valid_results.append(True)  # Treat None as valid
        else:
            # If an exception rises, the execution of the function will stop, and thus validation
            valid_results.append(validator(db=db, value=value))

    return all(valid_results)
