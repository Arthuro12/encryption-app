import random
import secrets
from functools import wraps
from flask import Flask, Blueprint, url_for, render_template, redirect, request, session, flash
from markupsafe import escape

from src.models.database import db
from forms.authentication_form import AuthenticationForm
from forms.encryption_form import EncryptionForm
from src.encryption.caeser_cypher import CaesarCypher
from src.encryption.monoalpha_cypher import MonoAlphaCypher
from src.models.base import Base
from src.models.encrypted_string import EncryptedString
from src.utils.load_config import get_entry
import src.utils.validation as validation
from src.dao.user_dao import UserDAO
from src.dto.user_dto import UserDTO
from src.dao.caesar_cypher_dao import CaesarCypherDAO
from src.dto.caesar_cypher_dto import CaesarCypherDTO
from src.dao.monoalpha_cypher_dao import MonoAlphaCypherDAO
from src.dto.monoalpha_cypher_dto import MonoAlphaCypherDTO

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = secrets.token_hex(16)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{get_entry()}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

blueprint = Blueprint("blueprint", __name__)


def is_logged(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "username" in session:
            return func(*args, **kwargs)
        return render_template("forbidden.html")
    return wrapper


def register(username, password):
    user_dao = UserDAO(db)
    active_user = user_dao.filter_user_by_username(username)
    encoded_password = password.encode("utf-8")
    if active_user is None:
        hashed_password = validation.hash_password(encoded_password)
        user_dto = UserDTO(username, hashed_password)
        user_dao.save_user(user_dto)
        print("Registriert!")


@blueprint.route("/encryption", methods=["GET", "POST"])
@is_logged
def render_encryption_form():
    encryption_form = EncryptionForm(request.form)
    if request.method == "POST":
        cypher_type = encryption_form.encryption_type.data
        user_dao = UserDAO(db)
        active_user = user_dao.filter_user_by_username(session["username"])
        match cypher_type:
            case "caesar":
                vector = 0
                if request.form["vector"]:
                    vector = encryption_form.vector.data
                else:
                    vector = random.randrange(1, 1024)
                CaesarCypher.set_vector(vector)
                encrypted_text = CaesarCypher.encrypt_text(encryption_form.plain_text.data)
                curr_cypher_type = CaesarCypherDTO(vector)
                cypher_type_dao = CaesarCypherDAO(db)
                encrypted_string_model = EncryptedString(encrypted_text, encryption_form.plain_text.data)
                user_dao.add_encrypted_string_user_association(active_user, encrypted_string_model)
                cypher_type_dao.add_encrypted_string_cypher_type_association(curr_cypher_type, encrypted_string_model)
                return redirect(url_for("blueprint.render_encryption_result", result=encrypted_string_model.value,
                                        vector=CaesarCypher.vector))
            case "monoalpha":
                encrypted_text = MonoAlphaCypher.encrypt_text(encryption_form.plain_text.data)
                encrypted_string_model = EncryptedString(encrypted_text, encryption_form.plain_text.data)
                curr_cypher_type = MonoAlphaCypherDTO()
                cypher_type_dao = MonoAlphaCypherDAO(db)
                user_dao.add_encrypted_string_user_association(active_user, encrypted_string_model)
                cypher_type_dao.add_encrypted_string_cypher_type_association(curr_cypher_type,
                                                                             encrypted_string_model)
                return redirect(url_for("blueprint.render_encryption_result", result=encrypted_string_model.value))
            case _:
                print("Prüfen Sie bitte die von Ihnen ausgewählte Verschlüsselungsart!")
    return render_template("encryption_form.html", form=encryption_form)


@blueprint.route("/result", methods=["GET", "POST"])
@is_logged
def render_encryption_result():
    result = request.args.get("result")
    vector = request.args.get("vector")
    if vector is not None:
        return render_template("encryption_result.html", result=result, vector=vector)
    else:
        return render_template("encryption_result.html", result=result)


@blueprint.route("/")
def render_index():
    is_user_connected = False
    if "username" in session:
        is_user_connected = True
    return render_template("index.html", connected=is_user_connected)


@blueprint.route("/login", methods=["GET", "POST"])
def render_login_form():
    login_form = AuthenticationForm(request.form)
    if request.method == "POST":
        session["username"] = escape(login_form.username.data)
        user_dao = UserDAO(db)
        current_user = user_dao.filter_user_by_username(session["username"])
        if current_user is not None:
            is_password_match = validation.compare_passwords(login_form.password.data.encode("utf-8"),
                                                             current_user.password)
            if not is_password_match:
                flash("Sie haben ein falsches Password eingegeben.", "WRONG_PASSWORD")
                return redirect(url_for("blueprint.render_login_form"))
            return redirect(url_for("blueprint.render_index"))
        else:
            flash("Unbekannter Benuzername.", "UNKNOWN_USER")
            return redirect(url_for("blueprint.render_login_form"))
    return render_template("login_form.html", form=login_form)


@blueprint.route("/logout", methods=["GET", "POST"])
def render_logout_form():
    if request.method == "POST":
        session.pop("username", None)
        flash("Sie wurden abgemeldet.")
        return redirect(url_for("blueprint.render_index"))
    return render_template("logout_form.html")


@blueprint.route("/register", methods=["GET", "POST"])
def render_register_form():
    register_form = AuthenticationForm(request.form)
    if request.method == "POST":
        user_dao = UserDAO(db)
        current_user = user_dao.filter_user_by_username(register_form.username.data)
        if current_user is not None:
            flash("Ein Benutzer mit diesem Benutzername existiert schon.", "USERNAME_TAKEN")
            return redirect(url_for("blueprint.render_register_form"))
        else:
            user_dto = UserDTO(escape(register_form.username.data), escape(register_form.password.data))
            register(user_dto.username, user_dto.password)
            return render_template("index.html")
    return render_template("register_form.html", form=register_form)


@blueprint.route("/users")
@is_logged
def render_users():
    user_dao = UserDAO(db)
    usernames = user_dao.get_usernames()
    parsed_usernames = [username_list for usernames_tuples in usernames for username_list in usernames_tuples]
    return render_template("users.html", usernames=parsed_usernames)


with app.app_context():
    Base.metadata.create_all(bind=db.engine)
    app.register_blueprint(blueprint)

app.run()
