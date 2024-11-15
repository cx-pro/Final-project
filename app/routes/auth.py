from app.utils.imports import *
from flask import Blueprint
from flask import render_template as _rd
from app.models import UserM
from app.utils.user import User
from app import bcrypt

auth = Blueprint("auth", __name__)


def rd(name: str, **context: any) -> str:
    return _rd(f"auth/{name}", **context)


@auth.route("/login", methods=["post", "get"])
def __login():
    if request.method.lower() == "post":
        form = request.form
        email = form.get("email", "")
        password = form.get("password", "")
        if not (email and password):
            return rd("login.html", email=email, pasword=password, status="empty")
        result = UserM.query.filter_by(
            email=email).first()
        if result is None:
            return rd("login.html", email=email, status="invalid")
        if not bcrypt.check_password_hash(result.password, password):
            return rd("login.html", email=email, status="invalid")
        user = User()
        user.id = result.id
        login_user(user, form.get("remember-me") != None)
    if current_user.is_authenticated:
        return redirect(request.args.get("next", "/"))
    return rd("login.html")


@auth.route("/logout", methods=["post"])
@login_required
def __logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect("/")
