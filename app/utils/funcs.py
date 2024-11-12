from app.utils.imports import *
from app.models import UserM


def getUsers(): return {str(x.id): x for x in UserM.query.all()}


def get_file_extension(fn: str): return fn[-fn[::-1].index(".")-1:]
