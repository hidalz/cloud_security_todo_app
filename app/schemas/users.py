from pydantic import BaseModel, EmailStr

from app import schemas
from app.schemas.projects import Project
from app.schemas.tasks import Task


class UserBase(BaseModel):
    username: str
    email: EmailStr


class User(UserBase):
    # Notice that the User, the Pydantic model that will be used when reading a user
    # (returning it from the API) doesn't include the password.
    id: int
    disabled: bool
    tasks: list[Task] = []
    owned_projects: list[Project] = []
    collaborated_projects: list[Project] = []

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    # Notice that the UserInDB, the Pydantic model that will be used when writing a user
    # (creating it in the database) includes the password.
    hashed_password: str
