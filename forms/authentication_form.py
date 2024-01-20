from wtforms import Form, StringField, PasswordField, validators, ValidationError


class AuthenticationForm(Form):
    username = StringField("Benutzername", validators=[validators.Length(4, 10, "Die Länge des Benutzernamen darf, "
                                                                                "weder nicht kleiner als 4 noch größer "
                                                                                "als 10 sein."),
                                                       validators.DataRequired()],
                           id="username")
    password = PasswordField("Passwort", [validators.DataRequired()], id="password")

    def is_reserved_username(self, usernames):
        if self.username.data in usernames:
            return True
        else:
            return False
