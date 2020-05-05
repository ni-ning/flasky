# coding: utf-8

import datetime
from flask import url_for, session, request, redirect, flash, render_template, make_response, abort

from . import main
from .forms import NameForm
from .. import db
from ..models import User


# @main.before_request
# def bar():
#     print('*' * 10)
#
#
# @main.before_first_request
# def func():
#     print('#' * 10)


@main.route('/')
def index():
    print('$' * 20)
    print(url_for('main.user', name='linda', page=2, version=1,  _external=True))
    print(url_for('main.static', filename='css/style.css', _external=True))
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is:<br> {}</p>'.format(user_agent)


@main.route('/user', methods=['GET', 'POST'])
def user():
    form = NameForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.name.data).first()
        if u is None:
            u = User(username=form.name.data)
            db.session.add(u)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.user'))
    return render_template('user0.html', name=session.get('name'),
                           form=form, known=session.get('known', False))


@main.route('/bad')
def bad():
    return '<h1>Bad Request</h1>', 400


@main.route('/resp')
def resp():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '60')
    return response


@main.route('/red')
def red():
    return redirect('http://www.baidu.com')


@main.route('/ab')
def ab():
    abort(400)
    return 'Hello World!'


@main.route('/tpl')
def tpl_index():
    return render_template('index.html')


@main.route('/tpl/user', methods=['GET', 'POST'])
def tpl_user():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('main.tpl_user'))
    return render_template('user.html', name=session.get('name'), form=form,
                           current_time=datetime.datetime.utcnow())