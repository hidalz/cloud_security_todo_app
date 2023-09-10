"""SQLAlchemy models for users service. 

SQLAlchemy models are used to define the structure of the data that is stored in the database."""

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.relationships import ProjectCollaborators


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)

    tasks = relationship("Task", back_populates="owner")

    # User can own multiple projects
    owned_projects = relationship(
        "Project", back_populates="owner", foreign_keys="Project.owner_id"
    )

    # User can collaborate on multiple projects
    collaborated_projects = relationship(
        "Project",
        secondary=ProjectCollaborators,
        back_populates="collaborators",
    )
