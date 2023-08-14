from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.schemas.users import User, UserBase, UserCreate

router = APIRouter()
