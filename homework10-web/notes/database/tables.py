import sqlalchemy as sa  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore

Base = declarative_base()


class Users(Base):  # type: ignore
    """Таблица пользователей"""

    __tablename__ = "users"

    id = sa.Column(
        sa.Integer,
        primary_key=True,
    )
    nickname = sa.Column(sa.String)  # имя пользователя
    hashed_password = sa.Column(sa.String)  # хэшированный пароль
    notes_id = sa.Column(sa.String)  # список заметок, доступ к которым имеет пользователя
    disabled = sa.Column(sa.Boolean)


class Notes(Base):  # type: ignore
    """Таблица заметок"""

    __tablename__ = "notes"

    id = sa.Column(
        sa.Integer,
        primary_key=True,
    )
    body = sa.Column(sa.String)  # тело заметки
    owner = sa.Column(sa.String)  # владелец заметки
    id_people_with_acsess = sa.Column(sa.String)  # список id людей, которые имеют доступ к заметке
