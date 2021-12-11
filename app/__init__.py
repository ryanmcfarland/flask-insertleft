from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

from config import app_config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()

login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
login.login_message_category = "warning"

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.url_map.strict_slashes = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    from app.common import bp as common_bp
    app.register_blueprint(common_bp, cli_group=None)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.blog import bp as blog_bp
    app.register_blueprint(blog_bp, url_prefix='/blog')

    from app.rpg.shootout import bp as shootout_bp
    from app.rpg.beatcops import bp as beatcops_bp    
    from app.rpg.swn import bp as swn_bp

    app.register_blueprint(shootout_bp, url_prefix='/shootout')
    app.register_blueprint(beatcops_bp, url_prefix='/beatcops')
    app.register_blueprint(swn_bp, url_prefix='/swn')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.contact import bp as contact_bp
    app.register_blueprint(contact_bp)

    return app

