from app.utils.imports import *
from app.models import Role


class User(UserMixin):
    @property
    def level(self):
        return Role.query.filter_by(id=self.id).first().level
