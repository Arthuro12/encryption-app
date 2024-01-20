from abc import ABC, abstractmethod


class CypherTypeDAOService(ABC):
    @abstractmethod
    def add_encrypted_string_cypher_type_association(self, cypher_type, encrypted_string):
        pass

    @abstractmethod
    def filter_cypher_type_by_id(self, cypher_type_id):
        pass

    @abstractmethod
    def save_cypher_type(self, cypher_type):
        pass
