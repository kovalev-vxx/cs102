from database.tables import Users  # type: ignore
from sqlalchemy import insert, update  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from .auth import get_password_hash


def find_last_user_id(
    session: Session,
) -> int:
    """Поиск id last_user_id пользователя, зарегистрированного последним
    Возвращает id на один больше
    """
    last_user_id = session.query(Users).all()[-1].id
    free_id = last_user_id + 1
    return free_id


def registration_in_db(
    session: Session,
    nickname: str,
    password: str,
) -> None:
    """Регистрация пользователя в базе данных"""
    session.add(
        Users(
            id=find_last_user_id(session),
            nickname=nickname,
            hashed_password=get_password_hash(password),
            notes_id="",
            disabled=False,
        )
    )
    session.commit()
