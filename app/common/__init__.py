from flask import Blueprint

bp = Blueprint('common', __name__)

from . import decorators, utils, commands, email
