from flask import Blueprint

bp = Blueprint('beatcops', __name__)

from app.beatcops import models, forms, routes