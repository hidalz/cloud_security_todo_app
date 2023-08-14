from pydantic import BaseModel

# TODO: Add subtasks


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    priority: int = 0
    # No ORM mode here


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    """https://fastapi.tiangolo.com/tutorial/sql-databases/#create-pydantic-models-schemas-for-reading-returning"""

    id: int
    owner_id: int
    project_id: int | None = None

    class Config:
        orm_mode = True
