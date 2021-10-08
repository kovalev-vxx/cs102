from settings import settings
from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
)

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)


def get_session() -> Session:  # type: ignore
    session = Session()
    try:
        yield session
    finally:
        session.close()
