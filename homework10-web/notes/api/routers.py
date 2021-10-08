import typing as tp
from datetime import timedelta
from pprint import pprint

from database.database import get_session  # type: ignore
from database.tables import Notes, Users  # type: ignore
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.models import Note, Token, UserInDb  # type: ignore
from settings import settings
from sqlalchemy.orm import Session  # type: ignore

from .auth import authenticate_user, create_access_token, get_current_active_user
from .registration import registration_in_db

router = APIRouter(prefix="/notes")


@router.post(
    "/registration",
    response_model=None,
)
def registration(
    nickname: str,
    password: str,
    session: Session = Depends(get_session),
) -> None:
    """Регистрация пользователя в базе данных
    nickname - имя пользователя
    password - будущий пороль пользователя
    session - сессия с базой данных
    """
    registration_in_db(
        session,
        nickname,
        password,
    )


@router.post(
    "/create/note",
    response_model=Note,
)
def create_note(
    body: str,
    current_user: UserInDb = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Создание заметки  пользователем
    body - тело заметки
    current_user - пользователь, запрашивающий действие
    session - сессия с базой данных
    """
    # узнаём гарантированно свободный id для новой замети
    try:
        id_note = session.query(Notes).all()[-1].id + 1
    except IndexError:
        id_note = 1

    note = Note(
        **{
            "id": id_note,
            "body": body,
            "owner": current_user.nickname,
            "id_people_with_acsess": str(current_user.id),
        }
    )  # создаём из имеющихся данных экземпляр заметок

    user = (
        session.query(Users).filter(Users.id == current_user.id).all()[0]
    )  # получаем current_user в виде объекта SQLAlchemy
    if user.notes_id == "":
        user.notes_id = id_note  # если это первая заметка пользователя
    else:
        user.notes_id += "," + str(id_note)  # если это не первая заметка пользователя
    session.add(
        Notes(
            id=note.id,
            body=note.body,
            owner=note.owner,
            id_people_with_acsess=note.id_people_with_acsess,
        )
    )  # добавляем заметку в БД
    session.commit()
    return note


@router.post(
    "/redact/note",
    response_model=Note,
)
def redact_note(
    note_id: int,
    new_body: str,
    current_user: UserInDb = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Редактирование заметки с индексом note_id:
    замена старого body на new_body
    """
    try:
        note_from_table = (
            session.query(Notes).filter(Notes.id == int(note_id)).all()[0]
        )  # получение заметки в виде объекта SQLAlchemy
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not correct note id",
        )
    if note_from_table.owner == current_user.nickname:  # проверка на собственность
        note = Note(
            **{
                "id": note_id,
                "body": new_body,
                "owner": current_user.nickname,
                "id_people_with_acsess": note_from_table.id_people_with_acsess,
            }
        )  # создаём из имеющихся данных экземпляр заметок
        note_from_table.body = note.body
        session.commit()
        return note
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="It's not your note",
        )


@router.get("/get/my_notes", response_model=tp.Optional[tp.List[Note]])  # type: ignore
def get_my_notes(
    current_user: UserInDb = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Получение пользователем current_user списка своих заметок"""
    list_notes_id = current_user.notes_id.split(",")  # получаем id заметок, которыми владеет user

    if list_notes_id == [""]:  # делаем проверку на возможное отсутствие заметок у user
        return None
    list_notes_id = list(
        map(
            int,
            list_notes_id,
        )
    )  # переводим все id в списке из str в int
    list_notes = (
        session.query(Notes).filter(Notes.id.in_(list_notes_id)).all()
    )  # получаем список заметок
    for i in range(len(list_notes)):
        list_notes[i] = Note(
            **list_notes[i].__dict__
        )  # каждую заметку переводим из объекта SQLAlchemy в dict

    return list_notes


@router.post(
    "/share/my_note",
    response_model=None,
)
def share_my_note(
    note_id_for_sharing: str,
    id_people: int,
    current_user: UserInDb = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):

    """Шаринг пользователем current_user заметки с id note_id_for_sharing пользователю id_people"""

    try:
        note = (
            session.query(Notes).filter(Notes.id == int(note_id_for_sharing)).all()[0]
        )  # получение заметки в виде объекта SQLAlchemy
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not correct note id",
        )

    if note.owner == current_user.nickname:  # проверка на собственность

        # если пользователя с запрашиваемым id нет, то вызываем ошибку
        people = session.query(Users).filter(Users.id == id_people).all()
        if people == []:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not correct people id",
            )
        else:
            # в противном случае получаем пользователя, которому хотим передать заметку в виде объекта SQLAlchemy
            people = people[0]

            # расширяем у заметки список того, кому она принадлежит
            note.id_people_with_acsess += f",{id_people}"

            # если у того кому мы хотим передать заметку - это первая заметка ...
            if people.notes_id == "":
                people.notes_id += note_id_for_sharing
            else:
                people.notes_id += "," + note_id_for_sharing  # ... иначе ...
            session.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="It's not your note",
        )


@router.post(
    "/delete/my_note",
    response_model=None,
)
def delete_my_note(
    note_id_for_deleting: str,
    current_user: UserInDb = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Удаление заметки с id note_id_for_deleting пользователем current_user"""
    # проверка на корректность введенного id заметки
    try:
        note = session.query(Notes).filter(Notes.id == int(note_id_for_deleting)).all()[0]
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not correct note id",
        )

    # получение списка id людей, которые имеют доступ к заметке
    list_id_people_with_access = note.id_people_with_acsess.split(",")

    if note.owner == current_user.nickname:
        session.delete(note)
        for id in list_id_people_with_access:
            id = int(id)
            people = session.query(Users).filter(Users.id == id).all()[0]
            people_list_notes_id = people.notes_id.split(",")
            people_list_notes_id.remove(note_id_for_deleting)
            people.notes_id = ",".join(people_list_notes_id)
        session.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="It's not your note",
        )


@router.post(
    "/token",
    response_model=Token,
)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
) -> tp.Dict[str, str,]:
    """По большей части cmd+c, cmd+v из документации FastAPI"""
    user = authenticate_user(
        session,
        form_data.username,
        form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.nickname}, expires_delta=access_token_expires  # type: ignore
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
