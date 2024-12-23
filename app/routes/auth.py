from app.utils.imports import *
from flask import Blueprint
from flask import render_template as _rd
from app.models import UserM
from app.utils.user import User
from app import bcrypt
from app import db

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


@auth.route("/signup", methods=["post", "get"])
def __register():
    if request.method.lower() == "post":
        form = request.form
        email = form.get("email", "")
        name = form.get("name", "")
        password = form.get("password", "")
        repeat_password = form.get("repeat_password", "")
        if not (email and password and repeat_password and name):
            return rd("login.html", email=email, pasword=password, repeat_password=repeat_password, status="empty")
        result = UserM.query.filter_by(
            email=email).first()
        if result:
            return rd("login.html", email=email, status="invalid")
        if password != repeat_password:
            return rd("login.html", email=email, status="invalid2")
        db.session.add(UserM(email=email, name=name,
                       password=bcrypt.generate_password_hash(password),role_id=2))
        db.session.commit()
        result = UserM.query.filter_by(
            email=email).first()
        user = User()
        user.id = result.id
        login_user(user, form.get("remember-me") != None)
    if current_user.is_authenticated:
        return redirect(request.args.get("next", "/"))
    return rd("register.html")
