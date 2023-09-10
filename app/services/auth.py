from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

import app.db.database as db
from app.models.users import User
from app.schemas.auth import TokenData

########### HASHING ###########

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """Verify password.

    Args:
        plain_password: Plain password.
        hashed_password: Hashed password.

    Returns:
        bool: True if password is valid, otherwise False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Get password hash.

    Args:
        password (str): Password.

    Returns:
        str: Password hash.
    """
    return pwd_context.hash(password)


########### JWT ###########

SECRET_KEY = "920b415199a51731fbdfead8b913bf1cbfd917b039f9259ee81ee0b494b58bdb "
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create access token for user.

    Args:
        data (dict): User data.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


#### AUTH SERVICE ###########

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


# TODO: Possibly reduce coupling
def get_user(username: str, db: Session = Depends(db.get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user:
        return user


def authenticate_user(username: str, password: str, db: Session = Depends(db.get_db)):
    user = get_user(username, db)

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(db.get_db),
):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # type: ignore
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(username=token_data.username, db=db)  # type: ignore
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:  # type: ignore
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
