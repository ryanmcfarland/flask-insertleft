from flask import Blueprint

bp = Blueprint('contact', __name__, static_folder='static')

from app.contact import routes