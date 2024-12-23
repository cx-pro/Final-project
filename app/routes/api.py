from app.utils.imports import *
from flask import Blueprint
from flask import render_template as _rd

api = Blueprint("api", __name__, url_prefix="/api")



@api.route("/set-theme", methods=["post"])
def __set_theme():
    session["theme"] = request.form.get("theme", "light")
    return "OK"