class CaesarCypherDTO:

    def __init__(self, vector):
        self.__vector = vector

    @property
    def vector(self):
        return self.__vector

    @vector.setter
    def vector(self, vector):
        self.__vector = vector
