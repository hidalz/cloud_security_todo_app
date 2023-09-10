"""Schemas for auth service.

The schemas are used to define the structure of the data that is sent between the services."""

from pydantic import BaseModel


class Token(BaseModel):
    """Token schema."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data schema."""

    username: str | None = None
