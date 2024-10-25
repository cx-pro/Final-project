from os import environ
from os import _Environ
from app.models import Role


def config(key: str = "") -> (str | _Environ):
    if not key:
        return environ
    return environ.get(key, environ.get(key.upper(), environ.get(key.lower(), "")))


class setting:
    ADMIN_LEVEL = None

    def __init__(self) -> None:
        self.ADMIN_LEVEL = Role.query.filter_by(name="admin").first().level
