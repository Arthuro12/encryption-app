from sqlalchemy import ForeignKey, Table, Column, Integer

from src.models.base import Base

string_user_association = Table(
    "string_user",
    Base.metadata,
    Column("encrypted_string_id", Integer, ForeignKey("encrypted_string.id")),
    Column("user_id", Integer, ForeignKey("user.user_id"))
)

string_cypher_association = Table(
    "string_cypher",
    Base.metadata,
    Column("encrypted_string_id", Integer, ForeignKey("encrypted_string.id")),
    Column("cypher_type_id", Integer, ForeignKey("cypher_type.id"))
)
