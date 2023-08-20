from sqlalchemy.orm import Session

import app.models.tasks as models
import app.schemas.tasks as schemas

# TODO: Refactor!!! Para que dentro no haya el doble de metodos, interfaz?


def get_all_tasks(
    db: Session, owner_id: int, skip: int = 0, limit: int = 100
) -> list[models.Task]:
    return (
        db.query(models.Task)
        .filter(models.Task.owner_id == owner_id)  # type: ignore
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_task(db: Session, owner_id: int, task_id: int) -> models.Task:
    return (
        db.query(models.Task)
        .filter(
            models.Task.owner_id == owner_id
        )  # TODO: Check si esto no hace falta y solo con el task id hay authorization
        .filter(models.Task.id == task_id)  # type: ignore
        .first()
    )


# TODO: Rework for authorization, even if its an internal method
def get_subtask(db: Session, subtask_id: int) -> models.Subtask:
    return (
        db.query(models.Subtask)
        .filter(models.Subtask.id == subtask_id)  # type: ignore
        .first()
    )


def create_user_task(
    db: Session, task: schemas.TaskCreateModify, user_id: int
) -> models.Task:
    db_task = models.Task(**task.dict(), owner_id=user_id)  # type: ignore

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def update_task(
    db: Session, owner_id: int, task_id: int, task: schemas.TaskCreateModify
) -> models.Task:
    # TODO: Check clean or coupling
    db_task = get_task(db, owner_id=owner_id, task_id=task_id)

    db_task.title = task.title  # type: ignore
    db_task.description = task.description  # type: ignore
    db_task.priority = task.priority  # type: ignore

    db.commit()
    db.refresh(db_task)

    return db_task


def create_subtask(
    db: Session, parent_task_id: int, subtask: schemas.TaskCreateModify
) -> models.Subtask:
    db_subtask = models.Subtask(**subtask.dict(), parent_id=parent_task_id)  # type: ignore

    db.add(db_subtask)
    db.commit()
    db.refresh(db_subtask)

    return db_subtask


def update_subtask(
    db: Session, subtask_id: int, subtask: schemas.TaskCreateModify
) -> models.Subtask:
    db_subtask = get_subtask(db, subtask_id=subtask_id)

    db_subtask.title = subtask.title  # type: ignore
    db_subtask.description = subtask.description  # type: ignore
    db_subtask.priority = subtask.priority  # type: ignore

    db.commit()
    db.refresh(db_subtask)

    return db_subtask
