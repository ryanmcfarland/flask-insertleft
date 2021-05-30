import click

from app import db
from app.models import User,Role
from app.common import bp

#flask common create-user --name test --email test1
@bp.cli.command('create-user')
@click.option('--name', prompt="Enter user name")
@click.option('--email', prompt="Enter user email")
@click.option('--password', prompt="Enter user password")
def create_user(name, email, password):
    """Manually create new user."""
    u = User(username=name, email=email)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()

#flask common create-role --name test
@bp.cli.command('create-role')
@click.option('--role', prompt="Enter role name")
def create_role(role):
    """Manually Create new user role."""
    r = Role(name=role)
    db.session.add(r)
    db.session.commit()

#flask common create-role --name test
@bp.cli.command('append-role')
@click.option('--username', prompt="Enter username")
@click.option('--role', prompt="Enter role to append")
def append_role(username, role):
    """Manually Create new user role."""
    u = User.query.filter_by(username=username).first()
    u.append_role(role)
    db.session.commit()