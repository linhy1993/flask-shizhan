# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request

from movies.models import MaoyanMovie

mod = Blueprint('movie', __name__)


@mod.route('/')
def movies():
    page = request.args.get('page', 1, type=int)
    pagination = MaoyanMovie.query.paginate(page, per_page=8, error_out=False)
    movie_shown = pagination.items
    return render_template('index.html', movie_shown=movie_shown, pagination=pagination)


@mod.route('/<int:page>/')
def movie_pages(page=None):
    if page is None:
        page = 1
    pagination = MaoyanMovie.query.paginate(page=page, per_page=8)
    movie_shown = pagination.items
    return render_template('index.html', movie_shown=movie_shown, pagination=pagination)
