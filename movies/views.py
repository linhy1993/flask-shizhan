# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, flash
from flask import request
from flask_login import login_user, logout_user, login_required

from movies import db
from movies.form import LoginForm, RegisterForm
from movies.models import MaoyanMovie, Users

mod = Blueprint('movie', __name__)


@mod.route('/')
@mod.route('/login/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(name=form.name.data).first()
        if user is not None and user.pwd == form.pwd.data:
            login_user(user)
            return redirect(url_for('.movie_pages', page=1))
        else:
            return redirect(url_for('.user_login', form=form))
    return render_template('user_login.html', form=form)


@mod.route('/<int:page>/')
@login_required
def movie_pages(page=None):
    if page is None:
        page = 1
    pagination = MaoyanMovie.query.paginate(page=page, per_page=8)
    movie_shown = pagination.items
    return render_template('index.html', movie_shown=movie_shown, pagination=pagination)


@mod.route('/search/', methods=['GET'])
@login_required
def search():
    if request.method == 'GET':
        q = request.args.get('query')
        condition = request.args.get('condition')

        if not q or not condition:
            return render_template('search.html')

        movies_lst = []
        if condition == 'movie_name':
            movies_lst = MaoyanMovie.query.filter(MaoyanMovie.name.like(f'%{q}%')).order_by('score')
        elif condition == 'release_year':
            movies_lst = MaoyanMovie.query.filter(MaoyanMovie.release_time.contains(q)).order_by('release_time')
        elif condition == 'stars':
            movies_lst = MaoyanMovie.query.filter(MaoyanMovie.stars.contains(q)).order_by('score')
        elif condition == 'score':
            movies_lst = MaoyanMovie.query.filter(MaoyanMovie.score >= q).order_by('score')
        elif condition == 'category':
            movies_lst = MaoyanMovie.query.filter(MaoyanMovie.category.contains(q)).order_by('score')
        return render_template('search.html', movies_lst=movies_lst, request=request, query=q)
    return render_template('search.html')


@mod.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.user_login'))


@mod.route('/regist/', methods=['GET', 'POST'])
def user_regist():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = Users(name=form.name.data, pwd=form.pwd.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功')
        return redirect(url_for('.user_login', username=user.name))
    return render_template('user_regist.html', form=form)
