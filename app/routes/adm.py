from app.utils.imports import *
from flask import Blueprint
from flask import render_template as _rd
from app.utils.user import roles_required
from app.models import *
from app.utils.funcs import get_file_extension

adm = Blueprint("adm", __name__)


def rd(name: str, **context: any) -> str:
    return _rd(f"adm/{name}", **context)


@adm.route("/ctrl/")
@roles_required('admin')
def __ctrl():
    return rd("ctrl.html")


@adm.route("/ctrl/media")
@roles_required('admin')
def __media_list():
    return rd("media/list.html")


@adm.route("/ctrl/new", methods=["get", "post"])
@roles_required('admin')
def __new():
    if request.method.lower() == "post":
        form = request.form
        file = request.files.get("file")
        fp = f"app/media/{request.form.get("type")
                          }s/{str(uuid4())}{get_file_extension(file.filename)}"
        if Media.query.filter_by(name=form["name"]).first():
            return rd("media/create.html", error={"name_field": "此名稱已存在"})
        file.save(fp)
        db.session.add(
            Media(form["name"], Category.query.filter_by(name=form["type"]).first().id, fp, current_user.name))
        db.session.commit()
        return redirect(url_for("adm.__media_list"))
    return rd("media/create.html")


@adm.route("/ctrl/edit")
@roles_required('admin')
def __edit():
    return rd("media/create.html")


@adm.route("/ctrl/destroy")
@roles_required('admin')
def __destroy():
    return redirect(url_for("adm.__media_list"))
