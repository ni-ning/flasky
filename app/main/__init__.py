# coding: utf-8

from flask import Blueprint

from . import views, errors


main = Blueprint('main', __name__)
