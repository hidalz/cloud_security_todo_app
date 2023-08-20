"""Declares the many-to-many relationship between different models."""
from sqlalchemy import Column, ForeignKey, Integer, Table

from app.db.database import Base

ProjectCollaborators = Table(
    "project_collaborators",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
)
