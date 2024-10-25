from app.models import *
from app import db
from app import bcrypt
import os


def refreshObj(objd, obj):
    if objd:
        db.session.delete(objd)
        db.session.commit()
    db.session.add(obj)
    db.session.commit()


def runSeeder():
    try:
        os.remove("app/dbs/main.db")
        db.create_all()
    finally:
        refreshObj(Role.query.filter_by(
            name="admin").first(), Role("admin", 0))
        refreshObj(Role.query.filter_by(name="user").first(), Role("user", 1))
        refreshObj(UserM.query.filter_by(email="user@test.com").first(), UserM("user@test.com", "testuser",
                                                                               bcrypt.generate_password_hash("user"), 2))
        refreshObj(UserM.query.filter_by(email="admin@test.com").first(), UserM("admin@test.com", "testadmin",
                                                                                bcrypt.generate_password_hash("admin"), 1))
