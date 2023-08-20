from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.relationships import ProjectCollaborators


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    is_active = Column(Boolean, default=True)
    created_at = Column(String)
    updated_at = Column(String)

    tasks = relationship("Task", back_populates="project")

    # Project is owned by one user
    owner = relationship(
        "User", back_populates="owned_projects", foreign_keys=[owner_id]
    )

    # Project can have multiple collaborators
    collaborators = relationship(
        "User",
        secondary=ProjectCollaborators,
        back_populates="collaborated_projects",
    )
