# coding: utf-8

from flask import render_template
from flask_mail import Message

from . import mail

#
# def send_mail(to, subject, template, **kw):
#     msg = Message(app.config['FLASKY_SUBJECT_PREFIX'] + subject,
#                   sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
#     msg.body = render_template(template + '.txt', **kw)
#     msg.html = render_template(template, '.html', **kw)
#     mail.send(msg)