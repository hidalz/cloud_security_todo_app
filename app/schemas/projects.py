from datetime import datetime

from pydantic import BaseModel

from app.schemas.tasks import Task


# TODO: Add IAM on Project for collaborators
class ProjectBase(BaseModel):
    name: str


class Project(ProjectBase):
    id: int
    owner_id: int
    is_archived: bool
    created_at: datetime
    tasks: list[Task] = []

    class Config:
        orm_mode = True
