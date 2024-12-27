from app.utils.imports import *
from flask import Blueprint
from flask import render_template as _rd
from app.utils.user import roles_required
from app.models import *
from app.utils.funcs import get_file_extension
from app import bcrypt

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
    category = request.args.get("category", 0)
    return rd("media/list.html", media=list(Media.query.filter_by(category_id=category) if category else Media.query.all()))


@adm.route("/ctrl/media/<id>")
@roles_required("user")
def __show_media(id):
    return rd("media/show.html", media=Media.query.filter_by(id=id).first())


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


@adm.route("/ctrl/media/<int:id>/edit", methods=["get", "post"])
@roles_required('admin')
def __edit(id):
    if request.method.lower() == "post":
        form = request.form
        if Media.query.filter_by(name=form["name"]).first():
            return rd("media/create.html", m=Media.query.filter_by(id=id).first(), error={"name_field": "此名稱已存在"})
        Media.query.filter_by(id=id).update(
            {"name": form["name"], "uploader": current_user.name})
        db.session.commit()
        return redirect(url_for("adm.__media_list"))
    return rd("media/create.html", m=Media.query.filter_by(id=id).first())


@adm.route("/ctrl/media/<int:id>/destroy")
@roles_required('admin')
def __destroy(id):
    db.session.delete(Media.query.filter_by(id=id).first())
    db.session.commit()
    return redirect(url_for("adm.__media_list"))


@adm.route("/ctrl/member")
@roles_required('admin')
def __member():
    return rd("member/list.html", members=UserM.query.all(), role=Role.query, ac=sum([int(i.is_admin) for i in UserM.query.all()]))


@adm.route("/member/<id>/edit", methods=["get", "post"])
@roles_required('admin')
def __edit_member(id):
    old_user_query = UserM.query.filter_by(id=id)
    old_user = old_user_query.first()
    if request.method.lower == "post":
        if request.form["email"] != old_user.email and UserM.query.filter_by(email=request.form["email"]).first():
            return rd("member/create.html", roles=Role.query.all(), error={"email": "電子信箱已被使用"}, userM=UserM(request.form["email"], request.form["name"],
                                                                                                             request.form["password"], int(request.form["role_id"])))
        old_user_query.update({})

    return rd("member/create.html", userM=old_user, roles=Role.query.all())


@adm.route("/member/<id>/destroy")
@roles_required('admin')
def __destory_member(id):
    db.session.delete(UserM.query.filter_by(id=id).first())
    db.session.commit()
    return redirect(url_for("adm.__member"))


@adm.route("/member/create", methods=["get", "post"])
@roles_required('admin')
def __create_member():
    if request.method.lower() == "post":
        if UserM.query.filter_by(email=request.form["email"]).first():
            return rd("member/create.html", roles=Role.query.all(), error={"email": "電子信箱已被使用"}, userM=UserM(request.form["email"], request.form["name"],
                                                                                                             request.form["password"], int(request.form["role_id"])))
        db.session.add(UserM(request.form["email"], request.form["name"], bcrypt.generate_password_hash(
            request.form["password"]), int(request.form["role_id"])))
        db.session.commit()
        return redirect(url_for("adm.__member"))
    return rd("member/create.html", roles=Role.query.all())
