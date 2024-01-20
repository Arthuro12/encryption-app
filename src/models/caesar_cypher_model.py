from sqlalchemy import ForeignKey, Column, Integer

from src.models.cypher_type import CypherType


class CaesarCypherModel(CypherType):
    __tablename__ = "caesar_cypher"

    id = Column(Integer, ForeignKey("cypher_type.id"), primary_key=True)
    vector = Column(Integer, nullable=False)

    def __init__(self, vector):
        super().__init__()
        self.vector = vector

    __mapper_args__ = {
        "polymorphic_identity": __tablename__
    }
