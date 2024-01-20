from src.models.user import User


class UserDAO:

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add_encrypted_string_user_association(self, user, encrypted_string):
        user.encrypted_strings.append(encrypted_string)
        self.db_connection.session.commit()

    def filter_user_by_username(self, username):
        return self.db_connection.session.query(User).filter_by(username=username).first()

    def get_usernames(self):
        return self.db_connection.session.query(User.username).all()

    def save_user(self, user_dto):
        parsed_user = User(user_dto.username, user_dto.password)
        self.db_connection.session.add(parsed_user)
        self.db_connection.session.commit()
