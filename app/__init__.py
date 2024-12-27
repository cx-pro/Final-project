from gevent import monkey  # nopep8
monkey.patch_all()  # nopep8

from app.utils.imports import *

app = Flask(__name__)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'auth.__login'
login_manager.refresh_view = 'auth.__login'
login_manager.REMEMBER_COOKIE_HTTPONLY = True
login_manager.REMEMBER_COOKIE_REFRESH_EACH_REQUEST = True

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////workspaces/Final-project/app/dbs/main.db"
app.config["SECRET_KEY"] = os.urandom(999)

db = SQLAlchemy(app)
bcrypt = Bcrypt()


from app.utils.user import User  # nopep8
from app.utils.funcs import getUsers  # nopep8
from app.routes.api import api  # nopep8
from app.routes.adm import adm  # nopep8
from app.routes.web import web  # nopep8
from app.routes.auth import auth  # nopep8
from app.dbs.seeders.mainSeeder import runSeeder  # nopep8
from app.utils.config import config  # nopep8
from app.utils.config import setting  # nopep8
app.register_blueprint(adm)
app.register_blueprint(api)
app.register_blueprint(auth)
app.register_blueprint(web)
DEFAULT_NAMESPACE["enumerate"] = enumerate
DEFAULT_NAMESPACE["config"] = config
DEFAULT_NAMESPACE["setting"] = setting
DEFAULT_NAMESPACE["int"] = int

with app.app_context():
    # db.create_all()
    runSeeder()


@login_manager.user_loader
def uloader(user0):
    if not user0 in getUsers():
        return

    user = User()
    user.id = user0
    return user


@login_manager.request_loader
def rloader(r):
    user0 = r.form.get('user_id')
    users = getUsers()

    if not user0 in users:
        return
    user = User()
    user.id = user0

    user.is_authenticated = bcrypt.check_password_hash(
        users[user0].password, r.form['password'])

    return user


# @app.route("/site-map")
# def __site_map():
#     return jsonify([rule.endpoint for rule in app.url_map.iter_rules()])


http_server = WSGIServer(('0.0.0.0', int(os.environ.get("PORT", 3000))),
                         app,
                         log=sys.stdout)
