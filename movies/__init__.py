# -*- coding: utf-8 -*-
from flask import Flask
from movies.settings import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)

from movies import views
app.register_blueprint(views.mod)
