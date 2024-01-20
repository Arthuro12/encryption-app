import getpass

from src.encryption.caeser_cypher import CaesarCypher
from src.encryption.monoalpha_cypher import MonoAlphaCypher
import src.utils.validation as validation
from src.models.db_connection import DatabaseSingleton
from src.models.encrypted_string import EncryptedString
from src.dto.user_dto import UserDTO
from src.dao.user_dao import UserDAO
from src.dao.caesar_cypher_dao import CaesarCypherDAO
from src.dto.caesar_cypher_dto import CaesarCypherDTO
from src.dao.monoalpha_cypher_dao import MonoAlphaCypherDAO
from src.dto.monoalpha_cypher_dto import MonoAlphaCypherDTO

props = {
    "username": "",
}


def get_confirmed(decision):
    decision_lower = decision.lower()
    if decision_lower == "ja":
        return True
    elif decision_lower == "nein":
        return False


def login(user):
    print("\nLoggen sie sich mit Ihrem Benutzername und Ihrem Passwort ein bitte:")
    username = input("Benutzername: \n")
    props["username"] = username
    # plain_text_password = getpass.getpass(prompt="Passwort: \n")
    plain_text_password = input("Password: \n")
    encoded_password = plain_text_password.encode("utf-8")
    active_user = user.filter_user_by_username(username)
    if active_user is None:
        hashed_password = validation.hash_password(encoded_password)
        user_dto = UserDTO(username, hashed_password)
        user.save_user(user_dto)
        print("Ein Konto wurde für Sie angelegt!")
    else:
        is_password_match = validation.compare_passwords(encoded_password, active_user.password)
        while not is_password_match:
            print("Sie haben ein falsches Passwort eingegeben!")
            # plain_text_password = getpass.getpass(prompt="Geben Sie Ihr Passwort erneut ein: \n")
            plain_text_password = input("Geben Sie Ihr Passwort erneut ein: \n")
            encoded_password = plain_text_password.encode("utf-8")
            is_password_match = validation.compare_passwords(encoded_password, active_user.password)
        print("Anmeldung erfolgreich!")
    print("\nWillkommen " + username, "!")


def menu_explorer():
    db_connection = DatabaseSingleton()
    user_dao = UserDAO(db_connection)
    login(user_dao)
    print("Wählen Sie eine Option. Zum Auswählen, eingeben und mit ENTER bestätigen:")

    while True:
        print_menus()
        option = input("Option wählen: ")
        current_menu_display_decision = "ja"

        match option:
            case "1":
                while get_confirmed(current_menu_display_decision):
                    print("\nAuthoren:")
                    print("Arthur Foadjo | 571698")
                    print("Konstantin Regenhardt | 557060")
                    print("Wollen Sie im aktuellen Menü bleiben?")
                    current_menu_display_decision = validation.get_decision()
                    if not get_confirmed(current_menu_display_decision):
                        print("")
                        break
            case "2":
                print("\nSie befinden sich unter dem Menü \"Caesarverschlüsselung\"")
                while get_confirmed(current_menu_display_decision):
                    plain_text = input("Bitte geben Sie die zu verschlüsselnde Zeichenkette ein: \n")
                    authorised_plain_text = validation.get_authorised_text(plain_text, CaesarCypher.ALLOWED_CHARS)
                    CaesarCypher.set_vector()
                    encrypted_text = CaesarCypher.encrypt_text(authorised_plain_text)
                    encrypted_string_model = EncryptedString(encrypted_text, authorised_plain_text)
                    active_user = user_dao.filter_user_by_username(props["username"])
                    user_dao.add_encrypted_string_user_association(active_user, encrypted_string_model)
                    curr_cypher_type = CaesarCypherDTO(CaesarCypher.vector)
                    cypher_type_dao = CaesarCypherDAO(db_connection)
                    cypher_type_dao.add_encrypted_string_cypher_type_association(curr_cypher_type,
                                                                                 encrypted_string_model)
                    print("Schlüssel der Verschlüsselung: {}".format(CaesarCypher.vector))
                    print("Der kodierte String ist: " + encrypted_text)
                    print("Ihre Zeichenkette wurde verschlüsselt. Wollen Sie im aktuellen Menü bleiben?")
                    current_menu_display_decision = validation.get_decision()
                    if not get_confirmed(current_menu_display_decision):
                        print("")
                        break
            case "3":
                print("\nSie befinden sich unter dem Menü \"Monoalphabetische Substitution\"")
                while get_confirmed(current_menu_display_decision):
                    plain_text = input("Bitte geben Sie die zu verschlüsselnde Zeichenkette ein: \n")
                    authorised_plain_text = validation.get_authorised_text(plain_text, MonoAlphaCypher.ALLOWED_CHARS)
                    encrypted_text = MonoAlphaCypher.encrypt_text(authorised_plain_text)
                    encrypted_string_model = EncryptedString(encrypted_text, authorised_plain_text)
                    curr_cypher_type = MonoAlphaCypherDTO()
                    cypher_type_dao = MonoAlphaCypherDAO(db_connection)
                    cypher_type_dao.add_encrypted_string_cypher_type_association(curr_cypher_type,
                                                                                 encrypted_string_model)
                    print("Der kodierte String ist: " + encrypted_text)
                    print("Ihre Zeichenkette wurde verschlüsselt. Wollen Sie im aktuellen Menü bleiben?")
                    current_menu_display_decision = validation.get_decision()
                    if not get_confirmed(current_menu_display_decision):
                        print("")
                        break
            case "4":
                print("Programm beendet.")
                exit()
            case _:
                print("Eingabe wurde nicht erkannt.")


def print_menus():
    print("Menüs:")
    print("1 - About")
    print("2 - Caesarverschlüsselung")
    print("3 - Monoalphabetische Substitution")
    print("4 - Exit")
