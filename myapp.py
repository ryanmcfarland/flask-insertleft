from app import create_app, db
from app.models import Grocery, User, Sheet, Weapon

app = create_app()
#app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Grocery': Grocery, 'User': User, 'Sheet': Sheet, 'Weapon': Weapon }