# -*- coding: utf-8 -*-
from flask import Blueprint

mod = Blueprint('movie', __name__)


@mod.route('/')
def index():
    return 'Hello World!'
