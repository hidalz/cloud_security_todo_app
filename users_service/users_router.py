"""Users routes.

It contains the API routes operations for managing users. It validates the input data before,
performing any operation in the database. It does so by using the validators in the validators,
as well as Pydantic models.

The routes are protected by OAuth2 JWT tokens. The token is passed in the Authorization header
of the request. The token is validated by the get_current_active_user function in the auth module.

Docs: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

import common_components.database.db as db
import users_service.users_schemas as user_schema
import users_service.users_services as user_crud
from auth_service.auth_services import get_current_active_user
from common_components.utils.input_validators import validate_user

router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/", status_code=HTTP_201_CREATED, response_model=user_schema.User)
def create_user(user: user_schema.UserInDB, db: Session = Depends(db.get_db)) -> user_schema.User:
    """Create user.

    Args:
        user (user_schema.UserInDB): User data.
        db (Session, optional): Database session. Defaults to Depends(db.get_db).

    Returns:
        user_schema.User: User data.

    Raises:
        HTTPException: If the username or email is already registered.
    """
    validate_user(
        db=db,
        username=user.username.lower(),
        email=user.email.lower(),
        password=user.hashed_password,
    )

    return user_crud.create_user(db=db, user=user)


#### USERS ####
@router.get("/me", response_model=user_schema.User)
async def read_my_user(
    current_user: user_schema.User = Depends(get_current_active_user),
) -> user_schema.User:
    """Get current user.

    Args:
        current_user (user_schema.User, optional): Current user. Defaults to Depends(get_current_active_user).

    Returns:
        user_schema.User: User data.
    """
    return current_user


@router.delete("/me", status_code=HTTP_204_NO_CONTENT)
def delete_my_account(
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
) -> None:
    """Delete current user.

    Args:
        db (Session, optional): Database session. Defaults to Depends(db.get_db).
        current_user (user_schema.User, optional): Current user. Defaults to Depends(get_current_active_user).

    Raises:
        HTTPException: If the user does not exist.
    """

    validate_user(db=db, user_id=current_user.id)

    user_crud.delete_user_by_id(db, user_id=current_user.id)


@router.put("/me/details", response_model=user_schema.UserBase)
def update_account_details(
    user: user_schema.UserBase,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
) -> user_schema.UserBase:
    """Update current user details.

    Args:
        user (user_schema.UserBase): User data.
        db (Session, optional): Database session. Defaults to Depends(db.get_db).
        current_user (user_schema.User, optional): Current user. Defaults to Depends(get_current_active_user).

    Returns:
        user_schema.UserBase: User data.

    Raises:
        HTTPException: If the username or email is already registered.
    """
    validate_user(
        db=db,
        username=user.username,
        email=user.email,
        check_email_is_registered=False,
    )

    return user_crud.update_account_details(
        db, user_data_update=user, current_user_id=current_user.id
    )


@router.patch("/me/password")
def update_account_password(
    password_schema: user_schema.UserUpdatePassword,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
) -> dict:
    """Update current user password.

    Args:
        password_schema (user_schema.UserUpdatePassword): User data.
        db (Session, optional): Database session. Defaults to Depends(db.get_db).
        current_user (user_schema.User, optional): Current user. Defaults to Depends(get_current_active_user).

    Returns:
        dict: Message.

    Raises:
        HTTPException: If the user does not exist.
        HTTPException: If the password is incorrect.
    """
    validate_user(db=db, password=password_schema.new_password)

    user_crud.update_account_password(
        db, password_schema=password_schema, current_user_id=current_user.id
    )

    return {"detail": "Password updated successfully"}


# ADMIN ONLY

# @router.get("/", status_code=HTTP_200_OK, response_model=list[user_schema.User])
# def read_users(
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(db.get_db),
#     current_user: user_schema.User = Depends(get_current_active_user),
# ):
#     users = user_crud.get_users(db, skip=skip, limit=limit)
#     return users


# @router.get("/{user_id}", status_code=HTTP_200_OK, response_model=user_schema.User)
# def read_user(
#     user_id: int,
#     db: Session = Depends(db.get_db),
#     current_user: user_schema.User = Depends(get_current_active_user),
# ):
#     db_user = user_crud.get_user_by_id(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
