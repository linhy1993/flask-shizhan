# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
from movies import db
from movies.models import MaoyanMovie, clean_db, init_db

mod = Blueprint('movie', __name__)



@mod.route('/')
def movies():
    page = request.args.get('page', 1, type=int)
    pagination = MaoyanMovie.query.paginate(page, per_page=8, error_out=False)
    movie_shown = pagination.items
    return render_template('index.html', movie_shown=movie_shown, pagination=pagination)
