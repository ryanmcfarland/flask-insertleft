#https://flask.palletsprojects.com/en/1.1.x/cli/

import click

from flask import Blueprint
from app import db
from app.models import User

bp = Blueprint('command', __name__)

#flask create --name test --email test1
@bp.cli.command('create')
@click.option('--name', prompt="Enter name")
@click.option('--email', prompt="Enter email")
@click.option('--password', prompt="Enter password")
def create(name, email, password):
    u = User(username=name, email=email)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()