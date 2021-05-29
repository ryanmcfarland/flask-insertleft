from flask import Blueprint

bp = Blueprint('cv', __name__)

from app.cv import routes