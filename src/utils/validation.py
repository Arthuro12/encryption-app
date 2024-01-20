import re
import bcrypt


def compare_passwords(transformed_password, stored_password):
    is_match = bcrypt.checkpw(transformed_password, stored_password)
    return is_match


def get_authorised_text(text, allowed_chars):
    while is_include_unauthorised_chars(text, allowed_chars):
        print("Die eingegebene Zeichenkette enthält ein ungültiges Zeichen.")
        text = input("Bitte geben Sie eine neue Zeichenkette ein: \n")
    return text


def get_decision():
    decision = input("Ja oder Nein: ").lower()
    while decision != "ja" and decision != "nein":
        print("Mit \"Ja\" oder \"Nein\" antworten bitte!")
        decision = input("Ihre Antwort: ").lower()
    return decision


def hash_password(encoded_password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(encoded_password, salt)
    return hashed_password


def is_include_special_chars(val):
    if not re.findall("[!#$%&'()*+,-./:;<=>?@[\]^_`{|}~]", val):
        return True
    else:
        return False


def is_include_unauthorised_chars(val, authorized_chars):
    for char in val:
        if char == " ":
            continue
        if char not in authorized_chars:
            return True
    return False
