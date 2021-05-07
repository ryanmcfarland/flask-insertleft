import os

from app import create_app, db
from app.models import User, Sheet, Weapon, Entry

config_name = os.getenv('FLASK_ENV')
app = create_app(config_name)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Entry': Entry, 'Sheet': Sheet, 'Weapon': Weapon }