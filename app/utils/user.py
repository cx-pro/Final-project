from app.utils.imports import *
from app.models import Role
from app.models import UserM
from functools import wraps
from app.utils.config import setting


class User(UserMixin):
    @property
    def level(self):
        return self.role.level

    @property
    def role_id(self):
        return self.modal.role_id

    @property
    def role(self):
        return Role.query.filter_by(id=self.role_id).first()

    @property
    def is_admin(self):
        return self.level <= setting().ADMIN_LEVEL

    @property
    def modal(self):
        return UserM.query.filter_by(id=self.id).first()

    @property
    def name(self):
        return self.modal.name


def roles_required(role: str, debug=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if debug:
                return f(*args, **kwargs)
            if not current_user.is_authenticated:
                return redirect(url_for('auth.__login', next=request.full_path))
            if current_user.role.name != role:
                return redirect("/")
            return f(*args, **kwargs)
        return decorated_function
    return decorator
