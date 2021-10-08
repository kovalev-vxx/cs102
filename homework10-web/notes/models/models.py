import typing as tp

from pydantic import BaseModel


class UserWithIdOnly(BaseModel):
    """Базовый класс пользователя - только с id"""

    id: int

    # подлючение orm_mode
    class Config:
        orm_mode = True


class User(UserWithIdOnly):
    """Второй класс пользователя - со всем необходимым, но без пароля"""

    nickname: str  # имя пользователя
    notes_id: str  # список заметок, доступ к которым имеет пользователь
    disabled: bool


class UserInDb(User):
    """Последний класс пользователя - с паролем"""

    hashed_password: str  # хэшированный пароль


class Note(BaseModel):
    """Класс заметки"""

    id: int
    body: str  # тело заметки
    owner: str  # владелец заметки
    id_people_with_acsess: str  # списко id людей, которые имеют доступ к заметки

    # подлючение orm_mode
    class Config:
        orm_mode = True


class Token(BaseModel):
    """Класс токена"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: tp.Optional[str] = None
