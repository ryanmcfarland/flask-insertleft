import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
configdir = os.environ.get('CONFIG_DIR') or '/home/ryanm/code/flask-insertleft/insertleft'
load_dotenv(os.path.join(configdir, '.env'), verbose = True)
# Load this after the load-dotenv to grab media directory from config file
mediadir = os.environ.get('MEDIA_DIRECTORY') or os.path.join(basedir, 'media')

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(configdir, 'insertleft.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SHEETS_PER_USER=5
    BLOG_SNAPSHOT=3
    SHEETS_PER_PAGE=6
    UPLOAD_IMAGES_FOLDER = os.path.join(mediadir, 'images')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    ADMIN=os.environ.get('ADMIN') or 'insertleft@outlook.com'
    CV = os.environ.get('CV') or configdir

    # outlook mail server configuration - used within flask_mail
    MAIL_SERVER='smtp.office365.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')

    #reCAPTCHA verify for login and register - https://developers.google.com/recaptcha/docs/verify
    RECAPTCHA_SITE_KEY=os.environ.get('RECAPTCHA_SITE_KEY')
    RECAPTCHA_SECRET_KEY=os.environ.get('RECAPTCHA_SECRET_KEY')
    RECAPTCHA_SITE_VERIFY=os.environ.get('RECAPTCHA_SITE_VERIFY')


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    #SQLALCHEMY_ECHO = True
    TEMPLATES_AUTO_RELOAD = True
    POSTS_PER_PAGE=2



class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    POSTS_PER_PAGE=5

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
