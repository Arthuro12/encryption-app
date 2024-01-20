import src.utils.validation as validation
import string


class MonoAlphaCypher:
    ALLOWED_CHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

    @staticmethod
    def encrypt_text(plain_text):
        inverted_chars = MonoAlphaCypher.get_inverted_chars()
        encrypted_text = ""

        while validation.is_include_unauthorised_chars(plain_text, MonoAlphaCypher.ALLOWED_CHARS):
            print("Die eingegebene Zeichenkette enthält ein ungültiges zeichen.")
            plain_text = input("Bitte geben Sie eine neue Zeichenkette ein: \n")
        for char in plain_text:
            if char == " ":
                encrypted_text += " "
                continue
            plain_char_idx = MonoAlphaCypher.ALLOWED_CHARS.index(char)
            encrypted_text += inverted_chars[plain_char_idx]
        return encrypted_text

    @staticmethod
    def get_inverted_chars():
        return MonoAlphaCypher.ALLOWED_CHARS[::-1]
