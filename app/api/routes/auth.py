from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

import app.db.database as db
from app.models.users import User
from app.schemas.auth import Token
from app.services.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
)

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/token", response_model=Token)
def login_for_access_token(
    db: Session = Depends(db.get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(
        form_data.username.lower(),
        form_data.password,
        db,
    )

    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}