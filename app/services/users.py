from sqlalchemy.orm import Session

import app.models.users as models
import app.schemas.users as schemas
import app.services.auth as auth

# TODO: Add correct permissions and add some methods only for admin accounts -> IAM


def create_user(db: Session, user: schemas.UserInDB) -> models.User:
    password_db = auth.get_password_hash(user.hashed_password)
    db_user = models.User(
        username=user.username.lower(),
        email=user.email.lower(),
        hashed_password=password_db,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()
