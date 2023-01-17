from datetime import timedelta
from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

from sqlalchemy.orm import Session

from api.auth.security import PasswordHasher
from api.utils.login import get_user
from api.schema.token import Token
from api.db.database import get_db
from api.auth.token_handler import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
)


router = APIRouter()


def authenticate_user(username: str, password: str, db: Session):
    user = get_user(db=db, username=username)
    if user is None:
        return False
    if not PasswordHasher.verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/token", response_model=Token)
async def get_login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token_expiry = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expiry
    )

    return {"access_token": access_token, "token_type": "bearer"}


OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")


def get_current_user(
    token: str = Depends(OAuth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Please provide valid credentials",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username=username, db=db)

    if user is None:
        raise credentials_exception

    return user
