from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import Base
from src.models.utils.associations import string_cypher_association


class CypherType(Base):
    __tablename__ = "cypher_type"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    encrypted_strings = relationship("EncryptedString", secondary=string_cypher_association,
                                     back_populates="cypher_types")

    __mapper_args__ = {
        "polymorphic_identity": __tablename__,
        "polymorphic_on": "type"
    }
