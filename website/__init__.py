from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, environ
from flask_login import LoginManager
from .email_service import init_email

app = Flask(__name__)

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    database_url = environ.get('DATABASE_URL')
    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ResumeBuilder.db'

    app.config['MAIL_SERVER'] = environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = environ.get('MAIL_USE_TLS', True)
    app.config['MAIL_USERNAME'] = environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = environ.get('MAIL_DEFAULT_SENDER', 'noreply@resumebuilder.com')

    db.init_app(app)
    init_email(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    create_database(app)

    return app

from .models import *

def create_database(app):
    with app.app_context():
        db.create_all()
        print('Database initialized')
