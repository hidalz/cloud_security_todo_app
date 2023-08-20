# https://docs.pydantic.dev/latest/usage/postponed_annotations/
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class TaskCreateModify(BaseModel):
    title: str
    description: str | None = None
    priority: int = 0


class TaskBase(TaskCreateModify):
    id: int


class Subtask(TaskBase):
    parent_id: int

    class Config:
        orm_mode = True


class Task(TaskBase):
    """https://fastapi.tiangolo.com/tutorial/sql-databases/#create-pydantic-models-schemas-for-reading-returning"""

    owner_id: int
    project_id: int | None = None
    subtasks: list[Subtask] = []

    class Config:
        orm_mode = True
