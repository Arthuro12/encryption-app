import random
import src.utils.validation as validation
import string


class CaesarCypher:
    ALLOWED_CHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    vector = 1

    @staticmethod
    def encrypt_text(plain_text):
        encrypted_text = ""
        for char in plain_text:
            if char == " ":
                encrypted_text += " "
                continue
            plain_char_idx = CaesarCypher.ALLOWED_CHARS.find(char)
            list_len = len(CaesarCypher.ALLOWED_CHARS)
            secret_char_position = (plain_char_idx + CaesarCypher.vector) % list_len
            encrypted_text += CaesarCypher.ALLOWED_CHARS[secret_char_position]

        return encrypted_text

    @staticmethod
    def get_vector():
        parsed_vector = 0
        print("Zum Verschlüsseln Ihrer Zeichenkette ist ein Schlüssel im Intervall vom 1 bis 1024 erförderlich.")
        encryption_vector = input("Geben Sie den Schlüssel ein bitte \n(Sie können dieser Schritt überspringen "
                                  "und ein zufälliger Schlüssel generieren lassen): ")
        if encryption_vector != "":
            parsed_vector = int(encryption_vector)
            while parsed_vector < 1 or parsed_vector > 1024:
                print("Der Schlüssel soll im Intervall vom 1 bis 1024 ausgewählt werden!")
                encryption_vector = input("Geben Sie den Schlüssel erneut ein oder lassen sie es vom System generien: ")
                parsed_vector = int(encryption_vector) if encryption_vector != "" \
                    else random.randrange(1, 1024)
        else:
            parsed_vector = random.randrange(1, 1024)
        return parsed_vector

    @staticmethod
    def set_vector(encryption_vector=None):
        if encryption_vector is not None and 0 < encryption_vector <= 1024:
            CaesarCypher.vector = encryption_vector
        else:
            CaesarCypher.vector = CaesarCypher.get_vector()

