from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from config import Config
from logging.handlers import RotatingFileHandler
import logging
import os


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login = LoginManager()
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login.init_app(app)
    moment.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth_barber import bp as auth_barber_bp
    app.register_blueprint(auth_barber_bp, url_prefix='/auth/barber')

    from app.barber import bp as barber_bp
    app.register_blueprint(barber_bp, url_prefix='/barber')

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/barbershop.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Barbershop startup')

    return app

from app import models
