from app.utils.imports import *
from flask import Blueprint
from flask import render_template as _rd

api = Blueprint("api", __name__, url_prefix="/api")
