"""Schemas for users service. 

The schemas are used to define the structure of the data that is sent between the services (API)."""

from pydantic import BaseModel, EmailStr

from projects_service.projects_schemas import Project
from tasks_service.tasks_schemas import Task


class UserBase(BaseModel):
    """User base schema. Used to validate the input data when creating a user."""

    username: str
    email: EmailStr


class User(UserBase):
    """User schema. Used to return the user data.

    Notice that the User, the Pydantic model that will be used when reading a user
    (returning it from the API) doesn't include the password.
    """

    id: int
    disabled: bool
    tasks: list[Task] = []
    owned_projects: list[Project] = []
    collaborated_projects: list[Project] = []
    is_superuser: bool = False

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    """User in database schema. Used to return the user data from the database.

    Notice that the UserInDB, the Pydantic model that will be used when reading a user
    (returning it from the database) includes the hashed password.
    """

    hashed_password: str

    class Config:
        orm_mode = True


class UserUpdatePassword(BaseModel):
    """User update password schema. Used to validate the input data when updating a user password."""

    current_password: str
    new_password: str

    class Config:
        orm_mode = True
