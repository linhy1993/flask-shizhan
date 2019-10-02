# -*- coding: utf-8 -*-

from flask_login import UserMixin

from movies import db


# Create your models here.
class MaoyanMovie(db.Model):
    __tablename__ = "maoyan_movies"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    stars = db.Column(db.String)
    release_time = db.Column(db.String)
    score = db.Column(db.Float)
    img_url = db.Column(db.String)
    info = db.Column(db.String)
    category = db.Column(db.String)


class Users(UserMixin, db.Model):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    pwd = db.Column(db.String)
    email = db.Column(db.String)

    def __init__(self, name, pwd, email):
        self.name = name
        self.pwd = pwd
        self.email = email

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.name

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


def drop_db():
    db.drop_all()


def init_db():
    db.create_all()


def clean_db():
    db.session.query(MaoyanMovie).delete()
    db.session.commit()
