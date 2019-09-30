# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from movies.settings import Config

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['WTF_CSRF_SECRET_KEY'] = '123456'
app.config['SECRET_KEY'] = '123456'

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
login_manger = LoginManager()
login_manger.session_protection = 'strong'
login_manger.login_view = 'movies.user_login'
login_manger.init_app(app)

@login_manger.user_loader
def load_user(user_id):
    from models import Users
    return Users.query.get(int(user_id))

from movies import views

app.register_blueprint(views.mod)
