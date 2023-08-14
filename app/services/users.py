from sqlalchemy.orm import Session

import app.models.users as models
import app.schemas.users as schemas


def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        username=user.username, email=user.email, hashed_password=fake_hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
