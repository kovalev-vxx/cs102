import typing as tp
from scraputils import get_news
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

Base = declarative_base()
path_news_db = "sqlite:///news.db"
engine = create_engine(path_news_db, connect_args={"check_same_thread": False})
local_session = sessionmaker(autocommit=False, autoflush=False)


@tp.no_type_check
def get_session(engine: Engine) -> Session:
    local_session.configure(bind=engine)
    return local_session()


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


Base.metadata.create_all(bind=engine)


def duplicate_check(title, author, session):
    if session.query(News).filter(News.author == author).filter(News.title == title).all():
        return False
    return True


def update_label(id, label, session):
    item = session.query(News).get(id)
    item.label = label
    session.commit()


def upload_to_db(news_list, session):
    for item in news_list:
        author, title, url, points, comments = (
            item["author"],
            item["title"],
            item["url"],
            item["points"],
            item["comments"],
        )
        if duplicate_check(title=title, author=author, session=session):
            add_news = News(title=title, author=author, url=url, points=points, comments=comments)
            session.add(add_news)
    session.commit()
    session.close()


def get_fresh_news(session, url="https://news.ycombinator.com/newest", n_pages=1):
    count_of_news = session.query(News).count()
    news = get_news(url, n_pages)
    upload_to_db(news, session=session)
    if session.query(News).count() == count_of_news:
        n_pages += 1
        get_fresh_news(session=session, url=url, n_pages=n_pages)


def clear_without_label_news(session):
    without_label = session.query(News).filter(News.label == None).all()
    for item in without_label:
        session.delete(item)
    session.commit()
    session.close()


def clear_labels(session):
    news_with_labels = session.query(News).filter(News.label != None).all()
    for item in news_with_labels:
        item.label = None
    session.commit()
    session.close()
