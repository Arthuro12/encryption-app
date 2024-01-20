from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import Base
from src.models.utils.associations import string_user_association


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, unique=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    encrypted_strings = relationship("EncryptedString", secondary=string_user_association,
                                     back_populates="users")

    def __init__(self, username, password, **kw):
        super().__init__(**kw)
        self.username = username
        self.password = password
