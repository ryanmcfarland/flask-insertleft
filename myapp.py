from app import create_app, db
from app.models import User, Sheet, Weapon, Notes

app = create_app()
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SHEETS_PER_PAGE'] = 2

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Notes': Notes, 'Sheet': Sheet, 'Weapon': Weapon }