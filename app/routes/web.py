from app.utils.imports import *
from app.utils.funcs import get_file_directory
from app.utils.funcs import get_filename
from app.models import Media
from flask import Blueprint
from flask import render_template as _rd
from app.utils.user import roles_required
web = Blueprint("web", __name__)


def rd(name: str, **context: any) -> str:
    return _rd(f"web/{name}", **context)


@web.route("/")
def __index():
    return rd("index.html")


@web.route("/media")
@roles_required("user")
def __media():
    category = request.args.get("category", 0)
    return rd("media/list.html", media=sorted(Media.query.filter_by(category_id=category) if category else Media.query.all()))


@web.route("/media/<id>")
@roles_required("user")
def __show_media(id):
    return rd("media/show.html", media=Media.query.filter_by(id=id).first())


@web.route("/search")
@roles_required("user")
def __search_media():
    q = request.args.get("q", "").lower()
    return rd("search.html", media=[i for i in Media.query.all() if q in i.name.lower() or q in i.uploader.lower()])


@web.route("/media/source/<id>")
@roles_required("user")
def __get_media_source(id):
    media = Media.query.filter_by(id=id).first()
    return send_file("../"+media.path)
