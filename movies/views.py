# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from movies import db
from movies.form import LoginForm, RegisterForm
from movies.models import MaoyanMovie, Users
from flask import request

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


@mod.route('/search/')
def search():
    return render_template('search.html')


@mod.route('/contact/')
def contact():
    return render_template('contact.html')


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