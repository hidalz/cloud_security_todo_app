"""Schemas for tasks service. 

The schemas are used to define the structure of the data that is sent between the services (API)."""

# https://docs.pydantic.dev/latest/usage/postponed_annotations/
from __future__ import annotations

from pydantic import BaseModel


class TaskCreateModify(BaseModel):
    """Task base schema. Used to validate the input data when creating or updating a task."""

    title: str
    description: str | None = None
    priority: int = 0
    parent_id: int | None = None
    project_id: int | None = None


class Task(TaskCreateModify):
    """Task schema. Used to return the task data.

    https://fastapi.tiangolo.com/tutorial/sql-databases/#create-pydantic-models-schemas-for-reading-returning
    """

    id: int
    owner_id: int
    subtasks: list[Task] = []

    class Config:
        orm_mode = True
