from app.utils.imports import *
from app.models import Media
from flask import Blueprint
from flask import render_template as _rd

web = Blueprint("web", __name__)


def rd(name: str, **context: any) -> str:
    return _rd(f"web/{name}", **context)


@web.route("/")
def __index():
    return rd("index.html")


@web.route("/media")
def __media():
    category = request.args.get("category", 0)
    return rd("media/list.html", media=Media.query.filter_by(category_id=category) if category else Media.query.all())
