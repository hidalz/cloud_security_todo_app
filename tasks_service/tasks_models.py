"""SQLAlchemy models for tasks service. 

SQLAlchemy models are used to define the structure of the data that is stored in the database."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from common_components.database.db import Base


class Task(Base):
    """Task model."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    priority = Column(Integer)

    # User tasks
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")

    # Project tasks
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="tasks")

    # Subtasks
    parent_id = Column(Integer, ForeignKey("tasks.id"))

    parent = relationship(
        "Task",
        back_populates="subtasks",
        remote_side=[id],
        single_parent=True,
        passive_deletes=True,
    )
    subtasks = relationship(
        "Task",
        back_populates="parent",
        remote_side=[parent_id],
        cascade="all, delete-orphan",
    )
