from app.utils.imports import *
from flask import Blueprint
from flask import render_template as _rd

adm = Blueprint("adm", __name__)


def rd(name: str, **context: any) -> str:
    return _rd(f"adm/{name}", **context)
