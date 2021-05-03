
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
login.login_message_category = "warning"

#logging.basicConfig(level=logging.DEBUG)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.url_map.strict_slashes = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.shootout import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/shootout')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.command import bp as command_bp
    app.register_blueprint(command_bp, cli_group=None)

    return app

