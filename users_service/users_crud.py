"""This module contains the CRUD operations for the users service.

The functions are used by the API routes to perform CRUD operations in the database. Validation of
the input data is performed by the validators in the input_validators module."""

from sqlalchemy.orm import Session

import auth_service.auth_crud as auth
import users_service.users_models as models
import users_service.users_schemas as schemas


def create_user(db: Session, user: schemas.UserInDB) -> models.User:
    """Create user.

    Args:
        db (Session): Database session.
        user (schemas.UserInDB): User data.

    Returns:
        models.User: SQL Alchemy User model.
    """

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
    """Get users.

    Args:
        db (Session): Database session.
        skip (int, optional): Number of users to skip. Defaults to 0.
        limit (int, optional): Number of users to return. Defaults to 100.

    Returns:
        list[User]: List of SQL Alchemy User models.
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int) -> models.User:
    """Get user by ID.

    Args:
        db (Session): Database session.
        user_id (int): User ID.

    Returns:
        models.User: SQL Alchemy User model.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    """Get user by email.

    Args:
        db (Session): Database session.
        email (str): User email.

    Returns:
        models.User: SQL Alchemy User model.
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str) -> models.User:
    """Get user by username.

    Args:
        db (Session): Database session.
        username (str): User username.

    Returns:
        models.User: SQL Alchemy User model.
    """
    return db.query(models.User).filter(models.User.username == username).first()


def delete_user_by_id(db: Session, user_id: int) -> None:
    """Delete user by ID.

    Args:
        db (Session): Database session.
        user_id (int): User ID.
    """
    db_user = get_user_by_id(db, user_id=user_id)
    if db_user is None:
        return None

    db.delete(db_user)
    db.commit()


def update_account_details(
    db: Session, user_data_update: schemas.UserBase, current_user_id: int
) -> models.User | None:
    """Update current user details.

    Args:
        db (Session): Database session.
        user_data_update (schemas.UserBase): User data.
        current_user_id (int): Current user ID.

    Returns:
        models.User: SQL Alchemy User model.

    Raises:
        HTTPException: If the username or email is already registered.
    """
    db_user = get_user_by_id(db, user_id=current_user_id)

    # Validation is performed in route operation
    db_user.username = user_data_update.username.lower()  # type: ignore
    db_user.email = user_data_update.email.lower()  # type: ignore

    db.commit()
    db.refresh(db_user)

    return db_user


def update_account_password(
    db: Session, password_schema: schemas.UserUpdatePassword, current_user_id: int
) -> models.User | None:
    """Update current user password.

    Args:
        db (Session): Database session.
        password_schema (schemas.UserUpdatePassword): User data.
        current_user_id (int): Current user ID.

    Returns:
        models.User: SQL Alchemy User model.

    Raises:
        HTTPException: If the user does not exist.
    """
    db_user = get_user_by_id(db, user_id=current_user_id)

    # The hashed password in the db and the input one must match
    if not auth.verify_password(password_schema.current_password, db_user.hashed_password):
        return None

    if password_schema.new_password:
        db_user.hashed_password = auth.get_password_hash(password_schema.new_password)  # type: ignore

    db.commit()
    db.refresh(db_user)

    return db_user
