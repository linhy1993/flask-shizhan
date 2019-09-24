# -*- coding: utf-8 -*-
from flask import Flask
from movies.settings import Config
from flask_sqlalchemy import SQLAlchemy
from movies import views

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.register_blueprint(views.mod)

db = SQLAlchemy(app)
