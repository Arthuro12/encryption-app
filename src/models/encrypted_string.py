from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import Base
from src.models.utils.associations import string_user_association
from src.models.utils.associations import string_cypher_association


class EncryptedString(Base):
    __tablename__ = "encrypted_string"

    id = Column(Integer, primary_key=True)
    value = Column(String, nullable=False)
    value_before = Column(String, nullable=False)
    users = relationship("User", secondary=string_user_association, back_populates="encrypted_strings")
    cypher_types = relationship("CypherType", secondary=string_cypher_association,
                                back_populates="encrypted_strings")

    def __init__(self, value, value_before, **kw):
        super().__init__(**kw)
        self.value = value
        self.value_before = value_before
