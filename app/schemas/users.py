from pydantic import BaseModel, EmailStr, constr

from app.schemas.projects import Project
from app.schemas.tasks import Task


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """User creation schema.

    For security, the password won't be in the previous Pydantic model.
    This way, it won't be sent from the API when reading a user."""

    password: str


class User(UserBase):
    # Notice that the User, the Pydantic model that will be used when reading a user
    # (returning it from the API) doesn't include the password.
    id: int
    is_active: bool
    tasks: list[Task] = []
    projects: list[Project] = []

    class Config:
        orm_mode = True
