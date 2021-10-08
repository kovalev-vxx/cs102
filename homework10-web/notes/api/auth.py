import typing as tp
from datetime import datetime, timedelta

from database.database import get_session  # type: ignore
from database.tables import Users  # type: ignore
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt  # type: ignore
from models.models import TokenData, UserInDb  # type: ignore
from passlib.context import CryptContext  # type: ignore
from settings import settings
from sqlalchemy.orm import Session  # type: ignore

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="notes/token")


def get_user(
    session: Session,
    username: str,
) -> tp.Optional[UserInDb]:
    user = session.query(Users).filter(Users.nickname == username).all()
    if len(user) != 0:
        user_dict = user[0].__dict__
        return UserInDb(**user_dict)
    else:
        return None


def verify_password(
    plain_password,
    hashed_password,
):
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def get_password_hash(
    password,
):
    return pwd_context.hash(password)


def authenticate_user(
    session: Session,
    username: str,
    password: str,
) -> tp.Union[UserInDb, bool,]:
    user = get_user(
        session,
        username,
    )
    if user is None:
        return False
    if not verify_password(
        password,
        user.hashed_password,
    ):
        return False
    return user


def create_access_token(
    data: dict,
    expires_delta: tp.Optional[timedelta] = None,
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(
        session,
        username=token_data.username,
    )
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: UserInDb = Depends(get_current_user),
):
    if current_user.disabled:
        raise HTTPException(
            status_code=400,
            detail="Inactive user",
        )
    return current_user
