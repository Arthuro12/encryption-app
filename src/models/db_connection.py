import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.utils.load_config import get_entry
from src.models.base import Base


class MetaSingleton(type):
    """
    Creates an instance of the class, ensuring that the class is instantiated only once.
    """

    __instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instance:
            cls.__instance[cls] = super().__call__(*args, **kwargs)
        return cls.__instance[cls]


class DatabaseSingleton(metaclass=MetaSingleton):
    def __init__(self):
        target_dir = "C:\\Programmierung3-Projekt\\vl2024-ka\\instance"
        self.__engine = create_engine(f"sqlite:///" + os.path.join(target_dir, get_entry()))
        Session = sessionmaker(self.__engine)
        self.__session = Session()
        if not os.path.isfile("C:\\Programmierung3-Projekt\\vl2024-ka\\instance\\vl2024.db"):
            Base.metadata.create_all(self.__engine)

    @property
    def engine(self):
        return self.__engine

    @engine.setter
    def engine(self, engine):
        self.__engine = engine

    @property
    def session(self):
        return self.__session

    @session.setter
    def session(self, session):
        self.session = session

