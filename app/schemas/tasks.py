# https://docs.pydantic.dev/latest/usage/postponed_annotations/
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class TaskCreateModify(BaseModel):
    title: str
    description: str | None = None
    priority: int = 0
    parent_id: int | None = None
    project_id: int | None = None


class Task(TaskCreateModify):
    """https://fastapi.tiangolo.com/tutorial/sql-databases/#create-pydantic-models-schemas-for-reading-returning"""

    id: int
    owner_id: int
    subtasks: list[Task] = []

    class Config:
        orm_mode = True
