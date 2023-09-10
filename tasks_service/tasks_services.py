"""This module contains the tasks functions that are used to interact with the database. 

The functions are used by the API routes to perform CRUD operations in the database. Validation of 
the input data is performed by the validators in the input_validators module."""

from sqlalchemy.orm import Session

import tasks_service.tasks_models as models
import tasks_service.tasks_schemas as schemas


def get_all_own_tasks(
    db: Session, owner_id: int, skip: int = 0, limit: int = 100
) -> list[models.Task]:
    return (
        db.query(models.Task)
        .filter(models.Task.owner_id == owner_id)  # type: ignore
        .filter(
            models.Task.parent_id == None
        )  # Avoid repetition of subtasks showing up as tasks, as they are already nested Pydantic models
        .filter(models.Task.project_id == None)  # Avoid repetition of tasks in projects and user
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_task(db: Session, owner_id: int, task_id: int) -> models.Task:
    """Get task by  task_id and owner_id.

    It checks that the task exists and that the owner_id is the same as the one provided.

    If the task is a subtask, it will be retrieved as well. All the nested subtasks will be
    retrieved.
    """

    return (
        db.query(models.Task)
        .filter(models.Task.owner_id == owner_id)  # type: ignore
        .filter(models.Task.id == task_id)
        .first()
    )


def create_task(
    db: Session,
    task: schemas.TaskCreateModify,
    user_id: int,
) -> models.Task:
    db_task = models.Task(
        **task.model_dump(),
        owner_id=user_id,
    )  # type: ignore

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def update_task(
    db: Session, owner_id: int, task: schemas.TaskCreateModify, task_id: int
) -> models.Task:
    db_task = get_task(db, owner_id=owner_id, task_id=task_id)  # type: ignore

    db_task.title = task.title  # type: ignore
    db_task.description = task.description  # type: ignore
    db_task.priority = task.priority  # type: ignore
    db_task.parent_id = task.parent_id  # type: ignore
    db_task.project_id = task.project_id  # type: ignore

    db.commit()
    db.refresh(db_task)

    return db_task


def delete_task(db: Session, owner_id: int, task_id: int):
    db_task = get_task(db, owner_id=owner_id, task_id=task_id)

    db.delete(db_task)
    db.commit()
