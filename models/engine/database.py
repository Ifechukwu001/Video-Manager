"""Database ORM"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.video import Base, Video


class DBStorage:

    __session = None
    __engine = None

    def __init__(self):
        self.__engine = create_engine("sqlite:///server.db")

    def load(self):
        Base.metadata.create_all(self.__engine)
        factory_session = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(factory_session)
        self.__session = Session

    def new(self, obj: Video):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def all(self):
        self.__session.query(Video).all()

    def get(self, cls: Video, id: str):
        return self.__session.query(cls).filter_by(id=id).first()

    def close(self):
        self.__session.remove()
