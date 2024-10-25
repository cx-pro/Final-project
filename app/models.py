from app.utils.imports import *
from app import db


class Category(db.Model):
    __tablename__ = 'b_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


class Media(db.Model):
    __tablename__ = 'b_media'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    category_id = db.Column(db.Integer)
    path = db.Column(db.Text)
    uploader = db.Column(db.Text)
    created_at = db.Column(db.Text)
    updated_at = db.Column(db.Text)

    def __init__(self, name, category_id, path, uploader, created_at, updated_at):
        self.name = name
        self.category_id = category_id
        self.path = path
        self.uploader = uploader
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<Media %r>' % self.name


class UserM(db.Model):
    __tablename__ = 'b_User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True)
    name = db.Column(db.Text)
    password = db.Column(db.Text)
    role_id = db.Column(db.Integer)

    def __init__(self, email, name, password, role_id):
        self.email = email
        self.name = name
        self.password = password
        self.role_id = role_id

    def __repr__(self):
        return '<UserM %r>' % self.name


class Role(db.Model):
    __tablename__ = 'b_Role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    level = db.Column(db.Integer, unique=True)

    def __init__(self, name, level):
        self.name = name
        self.level = level

    def __repr__(self):
        return '<Role %r>' % self.name
