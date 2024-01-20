from src.dao.service.cypher_type_dao_service import CypherTypeDAOService
from src.models.caesar_cypher_model import CaesarCypherModel


class CaesarCypherDAO(CypherTypeDAOService):

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add_encrypted_string_cypher_type_association(self, cypher_type_dto, encrypted_string):
        parsed_cypher_type = CaesarCypherModel(cypher_type_dto.vector)
        self.save_cypher_type(parsed_cypher_type)
        parsed_cypher_type.encrypted_strings.append(encrypted_string)
        self.db_connection.session.commit()

    def filter_cypher_type_by_id(self, cypher_type_id):
        return self.db_connection.session.query(CaesarCypherModel).filter_by(id=cypher_type_id).first()

    def save_cypher_type(self, cypher_type):
        self.db_connection.session.add(cypher_type)
        self.db_connection.session.commit()
