# coding: utf-8

import os
import datetime
from flask import Flask, make_response, redirect, abort, request, \
    render_template, url_for, session, flash

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASKY_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


def send_mail(to, subject, template, **kw):
    msg = Message(app.config['FLASKY_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kw)
    msg.html = render_template(template, '.html', **kw)
    mail.send(msg)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    sex = db.Column(db.Boolean, default=False)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username




@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.before_request
def bar():
    print('*' * 10)


@app.before_first_request
def func():
    print('#' * 10)


@app.route('/')
def index():
    print('$' * 20)
    print(url_for('user', name='linda', page=2, version=1,  _external=True))
    print(url_for('static', filename='css/style.css', _external=True))
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is:<br> {}</p>'.format(user_agent)


@app.route('/user', methods=['GET', 'POST'])
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
        return redirect(url_for('user'))
    return render_template('user0.html', name=session.get('name'),
                           form=form, known=session.get('known', False))


@app.route('/bad')
def bad():
    return '<h1>Bad Request</h1>', 400


@app.route('/resp')
def resp():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '60')
    return response


@app.route('/red')
def red():
    return redirect('http://www.baidu.com')


@app.route('/ab')
def ab():
    abort(400)
    return 'Hello World!'


@app.route('/tpl')
def tpl_index():
    return render_template('index.html')


@app.route('/tpl/user', methods=['GET', 'POST'])
def tpl_user():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('tpl_user'))
    return render_template('user.html', name=session.get('name'), form=form,
                           current_time=datetime.datetime.utcnow())


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

