from datetime import datetime

from sqlalchemy.orm import Session

import app.models.projects as models
import app.schemas.projects as schemas


def get_project(db: Session, project_id: int) -> models.Project:
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_project_by_name(db: Session, name: str) -> models.Project:
    return db.query(models.Project).filter(models.Project.name == name).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100) -> list[models.Project]:
    return db.query(models.Project).offset(skip).limit(limit).all()


def create_user_project(
    db: Session, project: schemas.ProjectBase, user_id: int
) -> models.Project:
    db_project = models.Project(
        **project.dict(), owner_id=user_id, created_at=datetime.now()
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


def delete_project(db: Session, project_id: int):
    db_project = (
        db.query(models.Project).filter(models.Project.id == project_id).first()
    )

    db.delete(db_project)
    db.commit()


# def archive_project(db: Session, project_id: int) -> models.Project:
#     db_project = (
#         db.query(models.Project).filter(models.Project.id == project_id).first()
#     )
#     db_project.is_archived = True
#     db.commit()
#     db.refresh(db_project)
#     return db_project
