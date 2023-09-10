from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

import app.db.database as db
import app.schemas.users as user_schema
import app.services.users as user_crud
from app.services.auth import get_current_active_user
from app.services.validators import validate_user

router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/", status_code=HTTP_201_CREATED, response_model=user_schema.User)
def create_user(user: user_schema.UserInDB, db: Session = Depends(db.get_db)):
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
):
    return current_user


@router.delete("/me", status_code=HTTP_204_NO_CONTENT)
def delete_my_account(
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
):
    validate_user(db=db, user_id=current_user.id)

    user_crud.delete_user_by_id(db, user_id=current_user.id)


@router.put("/me/details", response_model=user_schema.UserBase)
def update_account_details(
    user: user_schema.UserBase,
    db: Session = Depends(db.get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
):
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
):
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
