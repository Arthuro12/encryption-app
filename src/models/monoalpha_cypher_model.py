from sqlalchemy import ForeignKey, Column, Integer

from src.models.cypher_type import CypherType


class MonoalphaCypherModel(CypherType):
    __tablename__ = "monoalpha_cypher"

    id = Column(Integer, ForeignKey("cypher_type.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": __tablename__
    }
