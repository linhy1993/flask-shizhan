# -*- coding: utf-8 -*-
from movies import db


# Create your models here.
class MaoyanMovie(db.Model):
    __tablename__ = "maoyan_movies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    stars = db.Column(db.String)
    release_time = db.Column(db.String)
    score = db.Column(db.Float)
    img_url = db.Column(db.String)


def init_db():
    db.drop_all()
    db.create_all()


def clean_db():
    db.session.query(MaoyanMovie).delete()
    db.session.commit()
