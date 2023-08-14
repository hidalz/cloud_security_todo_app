from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_archived = Column(Boolean, default=False)
    created_at = Column(String)

    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")
