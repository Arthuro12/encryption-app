from wtforms import Form, TextAreaField, SelectField, IntegerField, validators


class EncryptionForm(Form):

    encryption_choices = [("caesar", "Caesar-Verschlüsselung"), ("monoalpha", "Monoalphabetische Verschlüsselüng")]
    encryption_type = SelectField(id="encryption-type", choices=encryption_choices)
    vector = IntegerField(id="vector")
    plain_text = TextAreaField(validators=[validators.DataRequired()])
