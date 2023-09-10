"""Schemas for projects service. 

The schemas are used to define the structure of the data that is sent between the services (API)."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.schemas.tasks import Task


class ProjectBase(BaseModel):
    name: str
    description: str


class Project(ProjectBase):
    id: int
    owner_id: int
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    tasks: list[Task] = []
    collaborators_id: list[int] = []

    class Config:
        orm_mode = True
