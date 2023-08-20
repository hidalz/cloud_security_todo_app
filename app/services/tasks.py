from sqlalchemy.orm import Session

import app.models.tasks as models
import app.schemas.tasks as schemas

# TODO: Refactor!!! Para que dentro no haya el doble de metodos, interfaz?


def get_all_own_tasks(
    db: Session, owner_id: int, skip: int = 0, limit: int = 100
) -> list[models.Task]:
    return (
        db.query(models.Task)
        .filter(models.Task.owner_id == owner_id)  # type: ignore
        .filter(
            models.Task.parent_id == None
        )  # Avoid repetition of subtasks showing up as tasks, as they are already nested Pydantic models
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_task(db: Session, owner_id: int, task_id: int) -> models.Task:
    """Get task by id and owner_id.

    If the task is a subtask, it will be retrieved as well. All the nested subtasks will be
    retrieved."""
    return (
        db.query(models.Task)
        .filter(models.Task.owner_id == owner_id)
        .filter(models.Task.id == task_id)
        .first()
    )


def create_task(
    db: Session,
    task: schemas.TaskCreateModify,
    user_id: int,
) -> models.Task:
    # TODO: Review that the user is the owner or collaborator of project. And the same for parent task. Extra function
    db_task = models.Task(
        **task.model_dump(),
        owner_id=user_id,
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def update_task(
    db: Session, owner_id: int, task: schemas.TaskCreateModify
) -> models.Task:
    # TODO: Check clean or coupling
    # TODO: Add comprobation that the user is the owner of the task and project collaborator, extra function. Make PATCHs
    db_task = get_task(db, owner_id=owner_id, task_id=task.id)

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
