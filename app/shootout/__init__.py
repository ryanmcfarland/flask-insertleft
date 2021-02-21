from flask import Blueprint

bp = Blueprint('shootout', __name__)

from app.shootout  import routes