import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from pydantic import BaseModel

password_hash = PasswordHash.recommended()

DUMMY_PASS = password_hash.hash("dummypassword")
AUTH_PASS = password_hash.hash(os.getenv("FASTAPI_AUTH_PWD"))
AUTH_USER = os.getenv("FASTAPI_AUTH_USR")
SECRET_KEY = os.getenv("FASTAPI_AUTH_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("FASTAPI_AUTH_EXP", 30))

fake_users_db = {
    AUTH_USER: {
        "username": AUTH_USER,
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": AUTH_PASS,
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def authenticate_user(fake_db, username: str, password: str):    
    user = None
    if username in fake_db:
        user_dict = fake_db[username]
        user = UserInDB(**user_dict)
    if not user:
        password_hash.verify(password, DUMMY_PASS)
        return False
    if not password_hash.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def validate_token(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM],
            options={"require": ["exp", "sub"]},
        )
    except jwt.InvalidTokenError as exc:
        raise credentials_exception from exc

    username = payload["sub"]
    if not isinstance(username, str) or not username or username not in fake_users_db:
        raise credentials_exception
    if fake_users_db[username]["disabled"]:
        raise credentials_exception
    return token
